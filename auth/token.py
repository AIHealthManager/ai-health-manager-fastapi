import jwt
from datetime import datetime, timedelta, UTC
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from config import JWT_KEY
from schemas.user_schemas import User

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(user: User) -> str:
    payload = {
        "sub": user.id,
        "exp": datetime.now(UTC) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS),
    }
    encoded_jwt = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token is expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
