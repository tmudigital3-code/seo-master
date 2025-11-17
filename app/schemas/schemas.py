from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class KeywordBase(BaseModel):
    keyword: str
    target_url: str
    search_country: str
    volume: Optional[int] = None
    difficulty: Optional[float] = None
    cpc: Optional[float] = None
    intent: Optional[str] = None

class KeywordCreate(KeywordBase):
    pass

class KeywordUpdate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class RankingBase(BaseModel):
    keyword_id: int
    platform: str
    position: Optional[int] = None
    visibility_score: Optional[float] = None
    url: Optional[str] = None

class RankingCreate(RankingBase):
    pass

class Ranking(RankingBase):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

class ClusterBase(BaseModel):
    name: str
    intent: str
    topic_similarity: float

class ClusterCreate(ClusterBase):
    pass

class Cluster(ClusterBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class ForecastBase(BaseModel):
    keyword_id: int
    predicted_volume: float
    confidence_score: float
    forecast_date: datetime

class ForecastCreate(ForecastBase):
    pass

class Forecast(ForecastBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class ContentScoreBase(BaseModel):
    keyword_id: int
    title_score: Optional[float] = None
    meta_description_score: Optional[float] = None
    word_count: Optional[int] = None
    keyword_density: Optional[float] = None
    readability_score: Optional[float] = None
    overall_score: Optional[float] = None
    suggestions: Optional[str] = None

class ContentScoreCreate(ContentScoreBase):
    pass

class ContentScore(ContentScoreBase):
    id: int
    analyzed_at: datetime
    
    class Config:
        orm_mode = True

class AIOverviewBase(BaseModel):
    keyword_id: int
    platform: str
    included: bool
    answer_sentiment: Optional[str] = None
    content_length: Optional[int] = None
    optimal_prompt: Optional[str] = None

class AIOverviewCreate(AIOverviewBase):
    pass

class AIOverview(AIOverviewBase):
    id: int
    analyzed_at: datetime
    
    class Config:
        orm_mode = True

class CompetitorBase(BaseModel):
    name: str
    url: str

class CompetitorCreate(CompetitorBase):
    pass

class Competitor(CompetitorBase):
    id: int
    added_at: datetime
    
    class Config:
        orm_mode = True

class AlertBase(BaseModel):
    keyword_id: int
    alert_type: str
    message: str
    resolved: bool = False

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    triggered_at: datetime
    
    class Config:
        orm_mode = True