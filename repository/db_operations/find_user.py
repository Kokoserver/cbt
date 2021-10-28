from typing import Union
from starlette import status
from repository.db import db as UserCoolection
from odmantic.exceptions import DocumentNotFoundError, KeyNotFoundInDocumentError
from odmantic import ObjectId
from backend.user.schema import User
from repository.errors import ErrorResponse


class User_operations:
    @staticmethod
    async def find_user_by_ID(user_id: bytes):
        try:
            user = await UserCoolection.find_one(User, User.id == user_id)
            return user
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_user_by_email_or_matric(username: str):
        try:
            user = await UserCoolection.find_one(User,User.email==username or User.admission_details.matric_no == username)
            return user
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_user_by_Email(email: str):
        try:
            user = await UserCoolection.find_one(User, User.email == email)
            return user
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_all_active_user():
        try:
            user:list = await UserCoolection.find(User)
            return user
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_all_unadmitted_user():
        try:
            user = await UserCoolection.find(User, User.admission_details == None and User.is_admin == False)
            return user
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def check_user_status(user_id: ObjectId):
        try:
            user = await UserCoolection.find_one(User, User.id == user_id)
            return user if user.is_active else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def get_current_active_user(current_user: Union[ObjectId, str]):
        if not current_user.is_active:
            raise ErrorResponse.error(
                message="Inactive user", status_code=status.HTTP_400_BAD_REQUEST
            )
        return current_user

    @staticmethod
    async def get_all_user(skip:int = 0, limit:int=10):
        try:
            users = await UserCoolection.find(User, limit=limit, skip=skip, sort= User.id)
            return users if users else None
        except Exception:
            return False

    @staticmethod
    async def save_user(user: User):
        saved_user = await UserCoolection.save(User(**user.dict()))
        return saved_user if saved_user else False

    @staticmethod
    async def delete_user(user: User):
        deleted_user = await UserCoolection.delete(user)
        return True if deleted_user else False
