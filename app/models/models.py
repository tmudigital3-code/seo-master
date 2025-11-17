from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    target_url = Column(String)
    search_country = Column(String)
    volume = Column(Integer)
    difficulty = Column(Float)
    cpc = Column(Float)
    intent = Column(String)  # informational, commercial, transactional, navigational
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rankings = relationship("Ranking", back_populates="keyword")
    forecasts = relationship("Forecast", back_populates="keyword")
    content_scores = relationship("ContentScore", back_populates="keyword")
    ai_overviews = relationship("AIOverview", back_populates="keyword")

class Ranking(Base):
    __tablename__ = "rankings"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"))
    platform = Column(String)  # google, bing, youtube, gemini, chatgpt, etc.
    position = Column(Integer)
    visibility_score = Column(Float)  # 0-100 percentage
    url = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    keyword = relationship("Keyword", back_populates="rankings")

class Cluster(Base):
    __tablename__ = "clusters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    intent = Column(String)
    topic_similarity = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    keywords = relationship("ClusterKeyword", back_populates="cluster")

class ClusterKeyword(Base):
    __tablename__ = "cluster_keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"))
    keyword_id = Column(Integer, ForeignKey("keywords.id"))
    
    # Relationships
    cluster = relationship("Cluster", back_populates="keywords")
    keyword = relationship("Keyword")

class Forecast(Base):
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"))
    predicted_volume = Column(Float)
    confidence_score = Column(Float)
    forecast_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    keyword = relationship("Keyword", back_populates="forecasts")

class ContentScore(Base):
    __tablename__ = "content_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"))
    title_score = Column(Float)
    meta_description_score = Column(Float)
    word_count = Column(Integer)
    keyword_density = Column(Float)
    readability_score = Column(Float)
    overall_score = Column(Float)
    suggestions = Column(Text)  # JSON formatted suggestions
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    keyword = relationship("Keyword", back_populates="content_scores")

class AIOverview(Base):
    __tablename__ = "ai_overviews"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"))
    platform = Column(String)  # google_ai, bing_copilot, etc.
    included = Column(Boolean)  # Yes/No
    answer_sentiment = Column(String)
    content_length = Column(Integer)
    optimal_prompt = Column(Text)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    keyword = relationship("Keyword", back_populates="ai_overviews")

class Competitor(Base):
    __tablename__ = "competitors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    rankings = relationship("CompetitorRanking", back_populates="competitor")

class CompetitorRanking(Base):
    __tablename__ = "competitor_rankings"
    
    id = Column(Integer, primary_key=True, index=True)
    competitor_id = Column(Integer, ForeignKey("competitors.id"))
    keyword_id = Column(Integer, ForeignKey("keywords.id"))
    platform = Column(String)
    position = Column(Integer)
    visibility_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    competitor = relationship("Competitor", back_populates="rankings")
    keyword = relationship("Keyword")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"))
    alert_type = Column(String)  # dropped_position, new_competitor, etc.
    message = Column(Text)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    
    # Relationships
    keyword = relationship("Keyword")