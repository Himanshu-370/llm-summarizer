from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    text_content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)