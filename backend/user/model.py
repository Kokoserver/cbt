from typing import Optional
from odmantic import ObjectId
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from pydantic import BaseModel
from os import urandom

class BaseUser(BaseModel):
    firstname: str = Field(min_length=3)
    lastname: str = Field(min_length=3)
    phone: str = Field(max_length=14)
    email: EmailStr
    class Config:
        anystr_lower = True

class UpdateUserDetails():
    pass

    class Config:
        anystr_lower = True


class UserResponseBody(BaseUser):
    is_active: bool = False
    created_at: Optional[datetime] = datetime.now()
    class Config:
       anystr_lower = True


class Register(BaseUser):
    password: bytes = Field(..., min_length=5)
    confirmPassword: bytes = Field(..., min_length=5)
    class Config:
        anystr_lower = True


class ChangePassword(BaseModel):
    id: ObjectId
    password: bytes
    confirmPassword: bytes
    class Config:
        anystr_lower = True

class Login(BaseModel):
    username: str
    password: bytes
    class Config:
        anystr_lower = True

class Token(BaseModel):
    access_token: str
    token_type: Optional[str] = "bearer"


class ForgotPasswordLink(BaseModel):
    email: EmailStr
    class Config:
        anystr_lower = True


class TokenData(BaseModel):
    id: str
