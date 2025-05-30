from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentCreate(BaseModel):
    filename: str
    
class DocumentOut(BaseModel):
    id: int
    filename: str
    upload_time: datetime
    summary: Optional[str]
    
    class Config:
        orm_mode = True
        
class SummarizeRequest(BaseModel):
    doc_id: int
    
    