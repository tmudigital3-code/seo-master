import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime, timedelta
from app.models.models import Keyword, Ranking, Cluster, ClusterKeyword
from app.database.database import get_db

class KeywordAnalyzer:
    def __init__(self, db_session):
        self.db = db_session
    
    def cluster_keywords(self, keywords, n_clusters=5):
        """
        Cluster keywords based on similarity
        """
        # Extract keyword texts
        keyword_texts = [kw.keyword for kw in keywords]
        
        # Vectorize keywords using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(keyword_texts)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=min(n_clusters, len(keyword_texts)), random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_matrix)
        
        # Save clusters to database
        clusters = []
        for i in range(min(n_clusters, len(set(cluster_labels)))):
            cluster = Cluster(
                name=f"Cluster {i+1}",
                intent="mixed",
                topic_similarity=0.0
            )
            self.db.add(cluster)
            self.db.flush()
            clusters.append(cluster)
        
        # Assign keywords to clusters
        for keyword, label in zip(keywords, cluster_labels):
            cluster_keyword = ClusterKeyword(
                cluster_id=clusters[label].id,
                keyword_id=keyword.id
            )
            self.db.add(cluster_keyword)
        
        self.db.commit()
        return clusters
    
    def calculate_visibility_score(self, rankings):
        """
        Calculate visibility score based on rankings across platforms
        """
        visibility_scores = {}
        
        # Weight factors for different platforms
        weights = {
            'google': 1.0,
            'bing': 0.8,
            'youtube': 0.7,
            'gemini': 0.9,
            'chatgpt': 0.85,
            'perplexity': 0.75
        }
        
        for ranking in rankings:
            platform = ranking.platform.lower()
            position = ranking.position
            
            if position is not None and position > 0:
                # Calculate score based on position (higher position = lower score)
                score = max(0, (100 - (position * 5)))  # Max score 100, decreases by 5 per position
                weighted_score = score * weights.get(platform, 0.5)
                
                if ranking.keyword_id not in visibility_scores:
                    visibility_scores[ranking.keyword_id] = 0
                
                visibility_scores[ranking.keyword_id] += weighted_score
        
        # Normalize scores to 0-100 range
        for keyword_id in visibility_scores:
            visibility_scores[keyword_id] = min(100, visibility_scores[keyword_id] / len(weights))
        
        return visibility_scores

class ForecastEngine:
    def __init__(self, db_session):
        self.db = db_session
    
    def predict_keyword_trends(self, keyword_id, days_ahead=30):
        """
        Predict future keyword performance using time series analysis
        """
        # Get historical rankings for the keyword
        historical_rankings = self.db.query(Ranking).filter(
            Ranking.keyword_id == keyword_id
        ).order_by(Ranking.timestamp.desc()).all()
        
        if len(historical_rankings) < 5:
            # Not enough data for reliable prediction
            return None
        
        # Simple linear regression for demonstration
        # In practice, you would use Prophet or ARIMA
        timestamps = [r.timestamp.timestamp() for r in historical_rankings]
        positions = [r.position if r.position else 100 for r in historical_rankings]
        
        # Convert to numpy arrays
        X = np.array(timestamps).reshape(-1, 1)
        y = np.array(positions)
        
        # Fit linear regression model
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict future positions
        future_timestamp = datetime.now().timestamp() + (days_ahead * 24 * 60 * 60)
        predicted_position = model.predict([[future_timestamp]])[0]
        
        # Calculate confidence based on R^2 score
        confidence = model.score(X, y)
        
        return {
            'predicted_position': max(1, int(predicted_position)),
            'confidence_score': max(0, min(1, confidence)),
            'forecast_date': datetime.now() + timedelta(days=days_ahead)
        }