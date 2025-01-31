from fastapi import APIRouter, Query
from database import get_db
from models import ReviewHistory, Category, AccessLog
from sqlalchemy import func
from celery_tasks import save_access_log_task
from utils import generate_tone_sentiment

router = APIRouter(prefix='/reviews')

@router.get('/trends')
def get_trends():
    db = get_db()
    results = db.query(
        Category.id,
        Category.name,
        Category.description,
        func.avg(ReviewHistory.stars).label('average_star'),
        func.count(ReviewHistory.id).label('total_review') 
    ).join(ReviewHistory, Category.id == ReviewHistory.category_id) \
    .group_by(Category.id) \
    .order_by(func.avg(ReviewHistory.stars).desc()) \
    .limit(5) \
    .all()
    db.close()
    # save to logs
    save_access_log_task.apply_async(args=["GET /reviews/trends"])

    return [{"id": category.id, "name": category.name, "description": category.description, 
             "average_star": category.average_star, "total_review": category.total_review} for category in results]

@router.get('/')
async def get_reviews(category_id: str, page: int = Query(1, ge=1)):
    db = get_db()
    reviews = db.query(ReviewHistory).filter(ReviewHistory.category_id == category_id) \
        .order_by(ReviewHistory.created_at.desc()) \
        .offset((page - 1) * 15).limit(15).all()
    db.close()
    # Check for missing tone and sentiment, and use LLM if needed
    for review in reviews:
        if review.tone is None or review.sentiment is None:
            review.tone, review.sentiment = await generate_tone_sentiment(review.text, review.stars)

    # save to logs
    save_access_log_task.apply_async(args=[f"GET /reviews/?category_id={category_id}"])

    return [{
        "id": review.id,
        "text": review.text,
        "stars": review.stars,
        "review_id": review.review_id,
        "created_at": review.created_at,
        "tone": review.tone,
        "sentiment": review.sentiment,
        "category_id": review.category_id
    } for review in reviews]

@router.get('/logs')
async def get_logs():
    '''
    This endpoint is added by me, just to view the access logs, in case the need arises.
    '''
    db = get_db()
    logs = db.query(AccessLog).order_by(AccessLog.id.desc()).all()
    db.close()
    return [{
        "id": log.id,
        "text": log.text

    } for log in logs]
