from typing import List
from fastapi import APIRouter, status
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from odmantic.bson import ObjectId
from repository.authentication import create_access_token, get_current_user
from repository.password_hasher import Hasher
from backend.schema.userSchema import User
from repository.db import DATABASE
from backend.model.userModel import (
    BaseUser,
    UserRegister,
    UserLogin,
    PasswordResetLink,
    UpdatePassword,
    UpdateUser,
    UserResponse,
    # TokenResponse,
)

router = APIRouter(tags=["User"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def register_new_user(user: UserRegister):
    if user.password != user.confirmPassword:
        return JSONResponse(
            content={"message": {"password": "password do not match"}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    check_user: User = await DATABASE.find_one(User, User.email == user.email)
    if check_user is not None:
        return JSONResponse(
            content={"message": {"Notfound": "Account already exist"}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    hashed_password = Hasher.hash_password(user.password)
    user.password = hashed_password
    try:
        if await DATABASE.save(User(**user.dict())):
            return JSONResponse(
                content={"message": "Account was created successfully"},
                status_code=status.HTTP_201_CREATED,
            )
    except Exception:
        return JSONResponse(
            content={"message": {"ServerError": "Error creating new user"}},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin):
    check_user: User = await DATABASE.find_one(User, User.email == user.email)
    if not check_user:
        return JSONResponse(
            content={"message": {"NotFound": "Account does not exist"}},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    check_password = Hasher.verify_password(user.password, check_user.password)
    if not check_password:
        return JSONResponse(
            content={"message": {"password": "password does not match"}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    access_token = create_access_token(check_user)

    return {
        "message": "Successfully login",
        "user": BaseUser(**check_user.dict()).dict(),
        "token": access_token,
    }


@router.post("/authenticate", status_code=status.HTTP_200_OK)
async def open_api_login_user(
    user: OAuth2PasswordRequestForm = Depends(),
):
    check_user: User = await DATABASE.find_one(User, User.email == user.username)
    if not check_user:
        return JSONResponse(
            content={"message": {"NotFound": "Account does not exist"}},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    check_password = Hasher.verify_password(user.password, check_user.password)
    if not check_password:
        return JSONResponse(
            content={"message": {"password": "password does not match"}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    access_token = create_access_token(check_user)
    print(access_token)

    return {
        "token_type": "Bearer",
        "access_token": access_token,
    }


@router.post("/forgotpassword", status_code=status.HTTP_200_OK)
async def password_reset_link(user: PasswordResetLink):
    pass


@router.post("/resetpassword", status_code=status.HTTP_200_OK)
async def password_reset(user: UpdatePassword):
    pass


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_user(user: UpdateUser):
    if user.is_active or user.is_admin:
        check_user = await DATABASE.find_one(User, User.email == user.email)
        if check_user:
            check_user.email = user.email
            check_user.firstname = user.firstname
            check_user.lastname = user.lastname
            await DATABASE.save(check_user)
            return JSONResponse({"message": "User was updated successfully"})
        return JSONResponse(
            {"NotFound": "user does not exist"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(
        {"AuthError": "Not authorized"}, status_code=status.HTTP_404_NOT_FOUND
    )


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_details(user: User = Depends(get_current_user)):
    return user


@router.get(
    "/alluser",
    response_model=List[User],
    response_model_exclude=["password"],
    status_code=status.HTTP_200_OK,
)
async def get_user_details(user: User = Depends(get_current_user)):
    if user.is_admin:
        all_user: User = await DATABASE.find(User)
        return all_user
    return JSONResponse(
        {"AuthError": "Not authorized"}, status_code=status.HTTP_401_UNAUTHORIZED
    )


@router.get(
    "/{userId}",
    response_model=User,
    response_model_exclude=["password"],
    status_code=status.HTTP_200_OK,
)
async def get_user_details(userId: ObjectId, user: User = Depends(get_current_user)):
    if user.is_admin:
        all_user: User = await DATABASE.find_one(User, User.id == userId)
        return all_user
    return JSONResponse(
        {"AuthError": "Not authorized"}, status_code=status.HTTP_401_UNAUTHORIZED
    )


@router.delete("/remove/{userId}", status_code=status.HTTP_204_NO_CONTENT)
async def get_user_details(userId: ObjectId, user: User = Depends(get_current_user)):
    if user.is_active or user.is_admin:
        user_to_be_remove = await DATABASE.find_one(User, User.id == userId)
        if user_to_be_remove:
            await DATABASE.delete(user_to_be_remove)
            return JSONResponse({"message": "user was removed successfully"})
        return JSONResponse(
            {"NotFound": "user does not exist"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return JSONResponse(
        {"NotFound": "Not authorized"}, status_code=status.HTTP_401_UNAUTHORIZED
    )
