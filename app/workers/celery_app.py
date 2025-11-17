from celery import Celery
import os

# Create Celery instance
celery_app = Celery("seo_tracker")

# Configure Celery
celery_app.conf.update(
    broker_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    result_backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_pool="solo"  # For Windows compatibility
)

# Auto-discover tasks
celery_app.autodiscover_tasks([
    "app.workers.tasks"
])