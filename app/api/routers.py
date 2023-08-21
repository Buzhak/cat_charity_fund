from fastapi import APIRouter

from app.api.endpoints.user import router as user_router
from app.api.endpoints.charity_project import router as charityproject_router
from app.api.endpoints.donation import router as donation_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(
    charityproject_router, prefix='/charity_project', tags=['Charity Project']
)
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donations']
)
