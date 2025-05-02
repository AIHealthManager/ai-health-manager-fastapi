from fastapi import APIRouter

from routers import google_auth_router, user_router, visit_router, profile_router


main_router = APIRouter()
main_router.include_router(google_auth_router.google_auth_router)
main_router.include_router(user_router.user_router)
main_router.include_router(visit_router.visit_router)
main_router.include_router(profile_router.profile_router)
