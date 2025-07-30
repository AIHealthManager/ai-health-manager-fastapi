from starlette.requests import Request
from fastapi import APIRouter, status, Depends
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from managers.user_manager import UserManager
from schemas.user_schemas import UserCreate
from auth.token import create_access_token
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, FRONT_END_GOOGLE_LOGIN_URL, GOOGLE_CALLBACK_URL
from db import get_db


google_sso = GoogleSSO(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_CALLBACK_URL,
    allow_insecure_http=True,
)

google_auth_router = APIRouter(prefix="/google-auth")


@google_auth_router.get("/login", tags=["Google SSO"])
async def google_login():
    return await google_sso.get_login_url(
        redirect_uri=GOOGLE_CALLBACK_URL,
        params={"prompt": "consent", "access_type": "offline"},
    )


@google_auth_router.get("/callback", tags=["Google SSO"])
async def google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    user = await google_sso.verify_and_process(request)
    user_stored = await UserManager.select_user_by_email(user.email, db)
    if not user_stored:
        user_to_add = UserCreate(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        user_stored = await UserManager.insert_user(user_to_add, db)
    token = create_access_token(user_stored)
    response = RedirectResponse(
        url=f"{FRONT_END_GOOGLE_LOGIN_URL}/google-auth?token={token}",
        status_code=status.HTTP_302_FOUND,
    )
    return response
