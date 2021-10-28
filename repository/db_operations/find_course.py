from odmantic import ObjectId
from repository.db import db as course_collection
from backend.course.schema import Course
from odmantic.exceptions import KeyNotFoundInDocumentError, DocumentNotFoundError


class Course_operations:
    @staticmethod
    async def find_course_by_ID(id: ObjectId):
        try:
            course = await course_collection.find_one(Course, Course.id == id)
            return course
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_course_by_title(title: str):
        try:
            course = await course_collection.find_one(Course, Course.title == title)
            return course
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def find_course_by_code(code: str):
        try:
            course = await course_collection.find_one(Course, Course.code == code)
            return course
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def filter_course(filterBy, filterType: str):
        try:
            if filterType == "semester":
                course = await course_collection.find_one(
                    Course, Course.semester == filterBy
                )
                return course
            if filterType == "unit":
                course = await course_collection.find_one(
                    Course, Course.unit == filterBy
                )
                return course
            if filterType == "level":
                course = await course_collection.find_one(
                    Course, Course.level == filterBy
                )
                return course
            if filterType == "status":
                course = await course_collection.find_one(
                    Course, Course.status == filterBy
                )
                return course
            if filterType == "id":
                course = await course_collection.find_one(
                    Course, Course.id == ObjectId(filterBy)
                )

                return course
            course = await course_collection.find()
            return course
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def check_course_semester(semester: str):
        try:
            course = await course_collection.find_one(
                Course, Course.semester == semester
            )
            return course if course else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def check_course_semester_and_level(
        semester: str, level:int
    ):
        try:
            course = await course_collection.find(
                Course,
                Course.semester == semester
                and Course.level == int(level)
            )
            return course if course else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    async def find_course_by_either(find_by: Course):
        try:
            course = await course_collection.find_one(
                Course, Course.title == find_by.title and Course.code == find_by.code
            )
            return course if course else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def get_all_course():
        try:
            course = await course_collection.find(Course)
            return course if course else False
        except DocumentNotFoundError:
            return False
        except KeyNotFoundInDocumentError:
            return False
        except Exception:
            return False

    @staticmethod
    async def save_course(course: Course):
        saved_course = await course_collection.save(Course(**course.dict()))
        return saved_course if saved_course else False

    @staticmethod
    async def delete_course(course: Course):
        deleted_course = await course_collection.delete(course)
        return True if deleted_course else False
