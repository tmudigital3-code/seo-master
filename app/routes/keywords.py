from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.schemas import Keyword, KeywordCreate, KeywordUpdate
from app.models.models import Keyword as KeywordModel

router = APIRouter(prefix="/keywords", tags=["keywords"])

@router.post("/", response_model=Keyword)
def create_keyword(keyword: KeywordCreate, db: Session = Depends(get_db)):
    db_keyword = KeywordModel(**keyword.dict())
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

@router.get("/{keyword_id}", response_model=Keyword)
def read_keyword(keyword_id: int, db: Session = Depends(get_db)):
    db_keyword = db.query(KeywordModel).filter(KeywordModel.id == keyword_id).first()
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return db_keyword

@router.get("/", response_model=List[Keyword])
def read_keywords(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    keywords = db.query(KeywordModel).offset(skip).limit(limit).all()
    return keywords

@router.put("/{keyword_id}", response_model=Keyword)
def update_keyword(keyword_id: int, keyword: KeywordUpdate, db: Session = Depends(get_db)):
    db_keyword = db.query(KeywordModel).filter(KeywordModel.id == keyword_id).first()
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    for key, value in keyword.dict().items():
        setattr(db_keyword, key, value)
    
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

@router.delete("/{keyword_id}")
def delete_keyword(keyword_id: int, db: Session = Depends(get_db)):
    db_keyword = db.query(KeywordModel).filter(KeywordModel.id == keyword_id).first()
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found")
    
    db.delete(db_keyword)
    db.commit()
    return {"message": "Keyword deleted successfully"}