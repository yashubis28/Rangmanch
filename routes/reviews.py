"""API routes for creating and managing Rangmanch reviews."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func

from models import Review, ReviewCreate, ReviewRead, ReviewUpdate
from database import get_session


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    """Create a review from validated request data."""
    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review 


@router.get("/", response_model=list[ReviewRead])
def list_reviews(
    play_name: str | None = Query(default=None, description="Filter reviews by play name"),
    skip: int = Query(default=0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of reviews to return"),
    session: Session = Depends(get_session)
):
    """List reviews, optionally filtering by play name and paginating results."""
    query = select(Review)
    if play_name:
        query = query.where(Review.play_name == play_name)
    query = query.offset(skip).limit(limit)   

    reviews = session.exec(query).all()

    return reviews


@router.get("/average-rating/{play_name}")
def get_average_rating(play_name: str, session: Session = Depends(get_session)):
    """Return the average rating and review count for a specific play."""
    result = session.exec(
        select(func.avg(Review.rating), func.count(Review.id)).where(
            Review.play_name == play_name
        )
    ).first()

    avg_rating, total_reviews = result

    if total_reviews == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No reviews found for the specified play: {play_name}",
        )
    return {"play_name": play_name, "average_rating": round(avg_rating, 2), "total_reviews": total_reviews}


@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, session: Session = Depends(get_session)):
    """Return one review by ID."""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.patch("/{review_id}", response_model=ReviewRead)
def update_review(review_id: int, review_update: ReviewUpdate, session: Session = Depends(get_session)):
    """Update only the fields included in the request."""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    update_data = review_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, session: Session = Depends(get_session)):
    """Delete a review and return no response body."""
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return None