from fastapi import APIRouter
from api.users.user_manager import current_active_user, current_admin_user
from api.users.models import User
from fastapi import Depends
from typing import List
from api.pois.reviews.schemas import ReviewCreate
from api.pois.reviews.dao import ReviewDAO

router = APIRouter(tags=["Points of interest", "POI Reviews"])


@router.post("{poi_id}/reviews", status_code=201)
async def create_review(poi_id: int, new_review: ReviewCreate):
    new_review.poi_id = poi_id
    ReviewDAO.insert_data(new_review)
