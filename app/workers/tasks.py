from celery import shared_task
from app.workers.scrapers import GoogleScraper, AIScraper, YouTubeScraper
from app.workers.analysis import KeywordAnalyzer, ForecastEngine
from app.database.database import get_db
from app.models.models import Keyword, Ranking
import time

@shared_task
def scrape_keyword_data(keyword_id):
    """
    Background task to scrape data for a keyword across all platforms
    """
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Get keyword from database
        keyword = db.query(Keyword).filter(Keyword.id == keyword_id).first()
        if not keyword:
            return {"status": "error", "message": "Keyword not found"}
        
        # Initialize scrapers
        google_scraper = GoogleScraper()
        ai_scraper = AIScraper()
        youtube_scraper = YouTubeScraper()
        
        # Scrape Google results
        google_results = google_scraper.get_search_results(keyword.keyword, keyword.search_country)
        
        # Save Google rankings
        for result in google_results:
            ranking = Ranking(
                keyword_id=keyword.id,
                platform="google",
                position=result['position'],
                url=result['url'],
                visibility_score=max(0, 100 - (result['position'] * 5))
            )
            db.add(ranking)
        
        # Scrape Google AI Overview
        ai_result = ai_scraper.get_google_ai_overview(keyword.keyword)
        ai_ranking = Ranking(
            keyword_id=keyword.id,
            platform="google_ai",
            position=1 if ai_result['included'] else None,
            visibility_score=90 if ai_result['included'] else 0
        )
        db.add(ai_ranking)
        
        # Scrape YouTube results
        youtube_results = youtube_scraper.get_video_rankings(keyword.keyword)
        
        # For simplicity, we'll just save the count as a ranking
        youtube_ranking = Ranking(
            keyword_id=keyword.id,
            platform="youtube",
            position=1 if youtube_results else None,
            visibility_score=min(100, len(youtube_results) * 10)
        )
        db.add(youtube_ranking)
        
        # Commit all changes
        db.commit()
        
        # Close scrapers
        ai_scraper.close()
        
        return {"status": "success", "keyword_id": keyword_id, "results_count": len(google_results) + len(youtube_results)}
    
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    
    finally:
        # Close database session
        try:
            next(db_gen, None)  # This will close the session
        except:
            pass

@shared_task
def analyze_keyword_cluster(keyword_ids):
    """
    Background task to cluster keywords and analyze them
    """
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Get keywords from database
        keywords = db.query(Keyword).filter(Keyword.id.in_(keyword_ids)).all()
        
        # Perform clustering analysis
        analyzer = KeywordAnalyzer(db)
        clusters = analyzer.cluster_keywords(keywords)
        
        db.commit()
        
        return {"status": "success", "clusters_created": len(clusters)}
    
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    
    finally:
        # Close database session
        try:
            next(db_gen, None)  # This will close the session
        except:
            pass

@shared_task
def generate_forecast(keyword_id):
    """
    Background task to generate forecast for a keyword
    """
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Generate forecast
        forecast_engine = ForecastEngine(db)
        forecast_data = forecast_engine.predict_keyword_trends(keyword_id)
        
        if forecast_data:
            # Here you would save the forecast to the database
            # For now, we'll just return the data
            return {"status": "success", "keyword_id": keyword_id, "forecast": forecast_data}
        else:
            return {"status": "warning", "message": "Not enough data for forecast"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    finally:
        # Close database session
        try:
            next(db_gen, None)  # This will close the session
        except:
            pass