# ----------------------------------------
# File: log_inputs_api.py
# ----------------------------------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

app = FastAPI()

#  SQLite DB path (keep consistent!)
DB_PATH = os.path.join("D:", "chatbotlangchain", "data", "translations.db")

Base = declarative_base()

#  Input table model
class InputRecord(Base):
    __tablename__ = "inputs"
    id = Column(Integer, primary_key=True, index=True)
    source_bn = Column(String, nullable=False)
    reference_en = Column(String, nullable=False)
    created_at = Column(String, nullable=False)

#  Engine + session
engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

#  Request model
class InputRequest(BaseModel):
    source_bn: str
    reference_en: str

#  POST route
@app.post("/log_input")
def log_input(req: InputRequest):
    try:
        db = SessionLocal()

        # Check if input pair already exists
        exists = db.query(InputRecord).filter(
            InputRecord.source_bn == req.source_bn.strip(),
            InputRecord.reference_en == req.reference_en.strip()
        ).first()

        if exists:
            db.close()
            return {"message": "Input already logged."}

        new_input = InputRecord(
            source_bn=req.source_bn.strip(),
            reference_en=req.reference_en.strip(),
            created_at=datetime.now().isoformat()
        )
        db.add(new_input)
        db.commit()
        db.close()

        return {"message": "Input logged successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
