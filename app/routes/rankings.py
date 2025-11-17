from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.schemas.schemas import Ranking, RankingCreate
from app.models.models import Ranking as RankingModel

router = APIRouter(prefix="/rankings", tags=["rankings"])

@router.post("/", response_model=Ranking)
def create_ranking(ranking: RankingCreate, db: Session = Depends(get_db)):
    db_ranking = RankingModel(**ranking.dict())
    db.add(db_ranking)
    db.commit()
    db.refresh(db_ranking)
    return db_ranking

@router.get("/{ranking_id}", response_model=Ranking)
def read_ranking(ranking_id: int, db: Session = Depends(get_db)):
    db_ranking = db.query(RankingModel).filter(RankingModel.id == ranking_id).first()
    if db_ranking is None:
        raise HTTPException(status_code=404, detail="Ranking not found")
    return db_ranking

@router.get("/", response_model=List[Ranking])
def read_rankings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rankings = db.query(RankingModel).offset(skip).limit(limit).all()
    return rankings