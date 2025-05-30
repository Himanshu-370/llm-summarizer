from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from . import models, schemas, crud, utils
import os
from dotenv import load_dotenv
import shutil

load_dotenv()

DATABASE_URL = "sqlite:///./documents.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "AI-powered Document Summarizer")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/upload", response_model=schemas.DocumentOut)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"temp_files/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
        
    if file.filename.endswith('.pdf'):
        text = utils.extract_text_from_pdf(file_location)
    elif file.filename.endswith('.docx'):
        text = utils.extract_text_from_docx(file_location)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    doc = crud.create_document(db=db, filename=file.filename, text_content=text)
    return doc

@app.get("/query", response_model=list[schemas.DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    return crud.list_documents(db=db)

@app.post("/summarize/{doc_id}", response_model=schemas.DocumentOut)
async def summarize(doc_id: int, db: Session = Depends(get_db)):
    doc = crud.get_document(db=db, doc_id=doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not doc.text_content:
        raise HTTPException(status_code=400, detail="Document has no text content to summarize")
    
    summary = await utils.summarize_text(doc.text_content)
    updated_doc = crud.update_document(db=db, doc_id=doc_id, summary=summary)
    
    return updated_doc