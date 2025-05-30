from sqlalchemy.orm import Session
from .models import Document

def create_document(db: Session, filename: str, text_content: str):
    doc = Document(filename=filename, text_content=text_content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def get_document(db: Session, doc_id: int):
    return db.query(Document).filter(Document.id == doc_id).first()

def list_documents(db: Session):
    return db.query(Document).all()

def update_document(db: Session, doc_id: int, summary: str):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if doc:
        doc.summary = summary
        db.commit()
        db.refresh(doc)
    return doc