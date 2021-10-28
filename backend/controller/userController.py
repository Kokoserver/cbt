from fastapi import status
from pydantic.networks import HttpUrl
from starlette.responses import Response
from backend.user.model import *
from backend.user.schema import User
from repository.password_hasher import Hasher
from repository.db_operations.find_user import User_operations
from repository.errors import ErrorResponse
from repository.authentication import create_access_token


async def get_user(user: User) -> User:
    """
    Get specific user ddetails by either ID or Email
    """
    # checking if user exist or not
    user: User = await User_operations.find_user_by_ID(user_id=user)
    if not user:
        # raise an error if user does not exist
        raise ErrorResponse.error(
            message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
        )
        # return user details if ut exist
    return user


async def create_user(user: Register) -> User:
    """
    Creating new user account, from them required details them submitted
    """
    # Checking user already exist or not
    verify_user = await User_operations.find_user_by_Email(email=user.email)
    if verify_user:
        # raise an error of user does bot exist
        raise ErrorResponse.error(
            message="User already exist", status_code=status.HTTP_400_BAD_REQUEST
        )
        # checking if user password matches
    if not user.password == user.confirmPassword:
        # raise an error if user password do not match
        raise ErrorResponse(
            message="Password do not macth", status_code=status.HTTP_400_BAD_REQUEST
        )
    # Generated hashed password for user
    password: bytes = Hasher.hash_password(user.password)
    # Updating user password to hashed one
    user.password = password

    # saving user new password
    new_user: User = await User_operations.save_user(user)
    # TODO send user confirmation email

    # checking if user saved succesfully
    if not new_user:
        # raise an error if was unable to save
        raise ErrorResponse.error(
            message="Error creating user account",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    # retuning new register details
    return new_user.dict()


async def login_user(user: Login) -> User:
    """
    Handlling User authentications, by taking there email and password checking for validations
    """
    # checking if user already exist or not
    verified_user: User = await User_operations.find_user_by_email_or_matric(username=user.username)
    # check if user detail is found
    if verified_user and verified_user.is_active:
        # verying if user password matches the hashed password
        verify_password: bool = Hasher.verify_password(
            plain_password=user.password, hashed_password=verified_user.password
        )
        # checking if pasword result was correct ot not
        if not verify_password:
            # raise an error if the password do not match
            raise ErrorResponse.error(
                message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
            )
        # generating authentication token for user
        token = create_access_token(data=verified_user)
        return {
            "user": UserResponseBody(**verified_user.dict()).dict(),
            "token": Token(access_token=token).dict(),
        }
    raise ErrorResponse.error(
        message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
    )

async def login_user_openApi(user: Login) -> User:
    """
    Handlling User authentications, by taking there email and password checking for validations
    """
    # checking if user already exist or not
    verified_user: User = await User_operations.find_user_by_email_or_matric(username=user.username)

    # check if user detail is found
    if verified_user and verified_user.is_active:
        # verying if user password matches the hashed password
        verify_password: bool = Hasher.verify_password(
            plain_password=user.password, hashed_password=verified_user.password
        )
        # checking if pasword result was correct ot not
        if not verify_password:
            # raise an error if the password do not match
            raise ErrorResponse.error(
                message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
            )
        # generating authentication token for user
        token = create_access_token(data=verified_user)
        return Token(access_token=token).dict(), token, UserResponseBody(**verified_user.dict()).dict()
        
    raise ErrorResponse.error(
        message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
    )


async def get_password_reset_link(userDetails: ForgotPasswordLink) -> dict:
    user: User = User_operations.find_user_by_Email(email=userDetails.email)
    if user:
        # TODO sent password reset link to user email
        return {"message": "Password reset link has been sent to your email"}
    raise ErrorResponse.error(
        message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
    )


async def update_user_password(userDetails: ChangePassword) -> User:
    """
    Updating user password by collecting there password and confirmpassword and ID
    """
    # checking if user exist
    user: User = User_operations.find_user_by_ID(user_id=userDetails.id)
    # checking if user details exist
    if not user:
        # raise an error if user does not exist
        raise ErrorResponse.error(
            message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
        )
    # Checking if  password matches
    if not userDetails.password == userDetails.confirmPassword:
        # raise an error if user password do not match
        raise ErrorResponse.error(
            message="Password do not macth", status_code=status.HTTP_400_BAD_REQUEST
        )
    # Generated hashed password for user if password matches
    password: bytes = Hasher.hash_password(user.password)
    # checking if password is generated
    if not password:
        raise ErrorResponse.error(
            message="Error updating password, plaease try agin",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    # Updating user password to hashed one
    user.password = password
    await User_operations.save_user(user)
    # returning updated user details
    return User_operations.find_user_by_ID(user_id=userDetails.id)


async def update_user_details(userdetails: User, admin_details: User):
    """
    Updating user password by collecting there password and confirmpassword and ID
    """
    if not admin_details.is_admin:
        raise ErrorResponse.error(
            message="Only admin can perform this operation",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # checking if user exist
    user: User = User_operations.find_user_by_Email(email=userdetails.email)
    # checking if user details exist
    if not user:
        # raise an error if user does not exist
        raise ErrorResponse.error(
            message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
        )
    user = userdetails
    update_user_details = await User_operations.save_user(user)
    if update_user_details:
        return update_user_details
    if not update_user_details:
        raise ErrorResponse.error(
            message="Error updating password, plaease try agin",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def delete_user(user: User, user_id: str) -> bool:
    """
    remove user from database system, this must be done by admin or an authorize person
    """
    # check if the operation was issue by an admin
    if not user.is_admin:
        raise ErrorResponse.error(
            message="Only admin can remove user",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    # checking user by ID
    user_to_be_removed: User = await User_operations.find_user_by_ID(
        user_id=ObjectId(user_id)
    )
    # checking if user exist
    if not user_to_be_removed and user_to_be_removed.is_admin:
        # raise and error if user does not exist
        raise ErrorResponse.error(
            message="User does not exist", status_code=status.HTTP_404_NOT_FOUND
        )
    # removing user from the databse system
    removed_user: any = await User_operations.delete_user(user_to_be_removed)
    if not removed_user:
        raise ErrorResponse.error(
            message="Error updating password, plaease try agin or consult the admin",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return True


async def all_user(admin:User):
    if not admin.is_admin:
        raise ErrorResponse.error(message="Only admin can perform this operation", status_code=status.HTTP_401_UNAUTHORIZED)
    all_user = await User_operations.find_all_active_user()
    if all_user:
        return all_user
    raise ErrorResponse.error(message="No user is found", status_code=status.HTTP_401_UNAUTHORIZED)


    
