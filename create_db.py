from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Translation(Base):
    __tablename__ = "translations"
    id = Column(Integer, primary_key=True)
    source_bn = Column(String)
    reference_en = Column(String)
    translation = Column(String)
    score = Column(Float)
    rank = Column(Integer)

engine = create_engine("sqlite:///D:/chatbotlangchain/data/translations.db")
Base.metadata.create_all(engine)

print(" DB created!")
