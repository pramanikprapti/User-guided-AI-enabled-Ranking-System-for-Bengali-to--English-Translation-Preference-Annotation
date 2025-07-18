import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

# ------------------------------
# 1. Ensure correct path
DB_DIR = os.path.join("D:", "chatbotlangchain", "data")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "translations.db")

# ------------------------------
# 2. SQLAlchemy setup
Base = declarative_base()

class Translation(Base):
    __tablename__ = "translations"
    id = Column(Integer, primary_key=True, index=True)
    source_bn = Column(String, nullable=False)
    reference_en = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)

# ------------------------------
# 3. Create DB
engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(bind=engine)
print(f" Database created at: {DB_PATH}")
