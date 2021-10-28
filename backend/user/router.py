from starlette.responses import Response
from backend.controller.userController import login_user
from fastapi import APIRouter, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from repository.authentication import get_current_user
from .model import *
from .schema import User
from backend.controller.userController import (
    get_user,
    all_user,
    create_user,
    update_user_password,
    delete_user,
    get_password_reset_link,
    login_user,
    login_user_openApi
)

router = APIRouter(prefix="/user", tags=["User"])

# getting user details
@router.get("/me", response_model=UserResponseBody, status_code=status.HTTP_200_OK)
# TODO implemetn token authentication so that i can get user details from the decode
async def user_detail(user: User = Depends(get_current_user)) -> dict:
    return user


# create user
@router.post(
    "/create", response_model=UserResponseBody, status_code=status.HTTP_201_CREATED
)
async def create_account(user: Register) -> dict:
    return await create_user(user)

@router.get("/alluser", status_code=status.HTTP_200_OK, response_model=list[UserResponseBody])
async def get_all_user(admin:User = Depends(get_current_user)):
    return await all_user(admin)



# login user for openApi
@router.post("/authenticate", include_in_schema=False)
async def Login_User_OpenApi(response:Response, userForm: OAuth2PasswordRequestForm = Depends()):
    user, token, user_detail = await login_user_openApi(user=Login(username=userForm.username, password=userForm.password))
    response.set_cookie(key="access_token",value=f"Bearer {token}", httponly=True)  #set HttpOnly cookie in response
    response.set_cookie(key="user", value=user_detail)
    return user


@router.post("/login")
async def Login_User(userData: Login):
    user = await login_user(user=userData)
    return user


# get password reset link
@router.post("/password/reset/link", status_code=status.HTTP_200_OK)
async def get_password_Reset_link(user: ForgotPasswordLink) -> dict:
    return get_password_reset_link(user)


# update user password
@router.put("/update/password", response_model=UserResponseBody, status_code=status.HTTP_200_OK)
async def update_password(user: ChangePassword):
    return await update_user_password(user)


# delete user
@router.delete("/", status_code=status.HTTP_200_OK)
async def remove_user(user_id: ObjectId, user: User = Depends(get_current_user)):
    return await delete_user(user, user_id)
