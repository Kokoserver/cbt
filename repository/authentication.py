from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from repository.db import DATABASE
from backend.model.userModel import TokenData
from backend.schema.userSchema import User
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/authenticate")


def create_access_token(data: User, expires_delta: Optional[timedelta] = None):
    user_data = data.dict()
    if user_data["id"]:
        user_data["id"] = str(user_data["id"])
    token_data = TokenData(**user_data).dict()
    to_encode = {"subs": token_data}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data = payload.get("subs")
        if not user_data:
            raise credentials_exception
        token_data = TokenData(email=user_data["email"])
    except JWTError:
        raise credentials_exception
    user = await DATABASE.find_one(User, User.email == token_data.email)
    if not user:
        raise credentials_exception
    return user
