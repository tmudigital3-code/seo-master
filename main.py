from fastapi import FastAPI
from app.routes import keywords, rankings
from app.database.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SEO Keyword Tracker", description="Advanced SEO dashboard that compares keyword performance across multiple AI platforms and search engines.")

# Include routers
app.include_router(keywords.router)
app.include_router(rankings.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the SEO Keyword Tracker API"}