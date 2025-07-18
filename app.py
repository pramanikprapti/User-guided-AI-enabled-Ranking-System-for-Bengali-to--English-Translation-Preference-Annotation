from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from comet.models import download_model, load_from_checkpoint
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# 1️⃣ FastAPI setup
app = FastAPI()

class TranslationRequest(BaseModel):
    source_bn: str
    reference_en: str

# 2️⃣ MarianMT or LLM pipeline
translation_pipe = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-bn-en"
)

# 3️⃣ COMET model
CACHE_DIR = os.path.join(os.getcwd(), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
comet_path = download_model("wmt21-comet-da", saving_directory=CACHE_DIR)
comet_model = load_from_checkpoint(comet_path)

# 4️⃣ SQLite setup
DB_PATH = os.path.join("D:", "chatbotlangchain", "data", "translations.db")
Base = declarative_base()

class Translation(Base):
    __tablename__ = "translations"
    id = Column(Integer, primary_key=True, index=True)
    source_bn = Column(String, nullable=False)
    reference_en = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)

engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

# 5️⃣ Route
@app.post("/translate_and_rank")
def translate_and_rank(req: TranslationRequest):
    try:
        # 🔹 Generate raw outputs
        outputs = translation_pipe(
            req.source_bn,
            num_beams=10,
            num_return_sequences=10,
            do_sample=True,
            top_k=50
        )

        # 🔹 Deduplicate
        translations = []
        seen = set()
        for o in outputs:
            t = o["translation_text"].strip()
            if t not in seen:
                seen.add(t)
                translations.append(t)
            if len(translations) == 5:
                break

        # 🔹 Pad if needed
        while len(translations) < 5:
            translations.append("[No unique translation generated]")

        # 🔹 Score with COMET
        data = [{"src": req.source_bn, "mt": t, "ref": req.reference_en} for t in translations]
        scores = comet_model.predict(data, gpus=0)['scores']

        # 🔹 Combine & rank
        results = [{"translation": t, "score": float(s)} for t, s in zip(translations, scores)]
        results.sort(key=lambda x: x["score"], reverse=True)
        for idx, item in enumerate(results, 1):
            item["rank"] = idx

        # 🔹 Store in DB
        db = SessionLocal()
        for item in results:
            db.add(Translation(
                source_bn=req.source_bn,
                reference_en=req.reference_en,
                translation=item["translation"],
                score=item["score"],
                rank=item["rank"]
            ))
        db.commit()
        db.close()

        return {
            "source_bn": req.source_bn,
            "reference_en": req.reference_en,
            "translations_ranked": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
