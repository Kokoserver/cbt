from odmantic import ObjectId
from pydantic import BaseModel, EmailStr, Field
from odmantic.bson import BaseBSONModel


class BaseUser(BaseModel):
    firstname: str = Field(min_length=3)
    lastname: str = Field(min_length=3)
    email: EmailStr
    is_active: bool = True
    is_admin: bool = True

    class Config:
        anystr_lower = True


class RegisterError(BaseModel):
    firstname: str = ""
    lastname: str = ""
    email: str = ""
    password: str = ""
    confirmPassword: str = ""


class UserResponse(BaseBSONModel):
    id: ObjectId
    firstname: str
    lastname: str
    is_active: bool
    is_admin: bool


class UserRegister(BaseUser):
    password: bytes = Field(min_length=5)
    confirmPassword: bytes = Field(min_length=5)

    class Config:
        anystr_lower = True


class UserLogin(BaseModel):
    email: EmailStr
    password: bytes

    class Config:
        anystr_lower = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user: UserResponse


class TokenData(BaseModel):
    email: str
    is_active: bool = False
    is_active: bool = False


class UpdatePassword(BaseModel):
    id: str

    class Config:
        anystr_lower = True


class UpdateUser1(BaseUser):
    id: str
    password: bytes = Field(min_length=5)
    confirmPassword: bytes = Field(min_length=5)


class UpdateUser(BaseUser):
    firstname: str = Field(min_length=3)
    lastname: str = Field(min_length=3)
    email: EmailStr

    class Config:
        anystr_lower = True


class PasswordResetLink(BaseUser):
    email: EmailStr

    class Config:
        anystr_lower = True


class CandidateLogin(BaseModel):
    matric_no: str
    password: str
    phone: str
