from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from odmantic import ObjectId
from backend.user.model import TokenData
from backend.user.schema import User
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from repository.db_operations.find_user import User_operations
from repository.utils import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="api/user/authenticate")

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
        token_data = TokenData(id=user_data["id"])
    except JWTError:
        raise credentials_exception
    user = await User_operations.find_user_by_ID(user_id=ObjectId(token_data.id))
    if not user:
        raise credentials_exception
    return user

