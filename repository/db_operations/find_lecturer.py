from typing import Union
from starlette import status
from repository.db import db as lecturerCoolection
from odmantic.exceptions import DocumentNotFoundError, KeyNotFoundInDocumentError
from odmantic import ObjectId
from backend.lecturer.schema import Lecturer
from repository.errors import ErrorResponse


class lecturer_operations:
    @staticmethod
    async def find_lecturer_by_ID(lecturer_id: bytes):
        try:
            lecturer = await lecturerCoolection.find_one(
                Lecturer, Lecturer.id == lecturer_id
            )
            return lecturer
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_lecturer_by_email_or_matric(lecturername: str):
        try:
            lecturer = await lecturerCoolection.find_one(
                Lecturer,
                Lecturer.email == lecturername
                or Lecturer.admission_details.matric_no == lecturername,
            )
            return lecturer
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_lecturer_by_Email(email: str):
        try:
            lecturer = await lecturerCoolection.find_one(
                Lecturer, Lecturer.email == email
            )
            return lecturer
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_all_active_lecturer():
        try:
            lecturer: list = await lecturerCoolection.find(Lecturer)
            return lecturer
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_all_unadmitted_lecturer():
        try:
            lecturer = await lecturerCoolection.find(
                Lecturer,
                Lecturer.admission_details == None and Lecturer.is_admin == False,
            )
            return lecturer
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def check_lecturer_status(lecturer_id: ObjectId):
        try:
            lecturer = await lecturerCoolection.find_one(
                Lecturer, Lecturer.id == lecturer_id
            )
            return lecturer if lecturer.is_active else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def get_current_active_lecturer(current_lecturer: Union[ObjectId, str]):
        if not current_lecturer.is_active:
            raise ErrorResponse.error(
                message="Inactive lecturer", status_code=status.HTTP_400_BAD_REQUEST
            )
        return current_lecturer

    @staticmethod
    async def get_all_lecturer(skip: int = 0, limit: int = 10):
        try:
            lecturers = await lecturerCoolection.find(
                Lecturer, limit=limit, skip=skip, sort=Lecturer.id
            )
            return lecturers if lecturers else None
        except Exception:
            return False

    @staticmethod
    async def save_lecturer(lecturer: Lecturer):
        saved_lecturer = await lecturerCoolection.save(Lecturer(**lecturer.dict()))
        return saved_lecturer if saved_lecturer else False

    @staticmethod
    async def delete_lecturer(lecturer: Lecturer):
        deleted_lecturer = await lecturerCoolection.delete(lecturer)
        return True if deleted_lecturer else False
