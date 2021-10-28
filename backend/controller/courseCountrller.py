from backend.user.schema import User
from fastapi import status
from odmantic.bson import ObjectId
from backend.course.schema import Course
from backend.course.model import Course as CourseModel, CourseUpdate, SaveCourse
from repository.db_operations.find_course import Course_operations
from repository.errors import ErrorResponse


async def all():
    all_courses = await Course_operations.get_all_course()
    if all_courses:
        return all_courses
    return []


async def get(filterBy: str, filterType: str):
    course = await Course_operations.filter_course(
        filterBy=filterBy, filterType=filterType
    )
    if course:
        return course
    raise ErrorResponse.error(
        message=f"course with {filterBy} doee not exist",
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def create(course: CourseModel, user: User):
    if not user.is_admin:
        raise ErrorResponse.error(
            message=f" Only admin can perform this operation",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    check_course = await Course_operations.find_course_by_either(find_by=course)
    if check_course:
        raise ErrorResponse.error(
            message=f"course with either {course.title}, {course.code} , already  exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    course_to_be_saved = Course(**course.dict())
    new_course = await Course_operations.save_course(course_to_be_saved)
    if new_course:
        return new_course
    raise ErrorResponse.error(
        message="Error savings this course", status_code=status.WS_1011_INTERNAL_ERROR
    )


async def update(course: CourseUpdate, user: User, courseId:str):
    if not user.is_admin:
        raise ErrorResponse.error(
            message=f" Only admin can perform this operation",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    get_course = await Course_operations.find_course_by_ID(id=ObjectId(courseId))
    if not get_course:
        raise ErrorResponse.error(
            message=f"course with ID '{courseId}' doee not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    course_to_update = SaveCourse(**course.dict(), id=ObjectId(courseId))
    if  get_course == course_to_update:
        raise ErrorResponse.error(
            message=f"course with {course.title}, {course.code} {course.semaster}, already  exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    get_course = course_to_update
    new_course = await Course_operations.save_course(get_course)
    if new_course:
        return new_course
    raise ErrorResponse.error(
        message=f"Error updating this course", status_code=status.WS_1011_INTERNAL_ERROR
    )


async def delete(courseId: str, user: User):
    if not user.is_admin:
        raise ErrorResponse.error(
            message=f" Only admin can perform this operation",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    course = await Course_operations.find_course_by_ID(id=ObjectId(courseId))
    if not course:
        raise ErrorResponse.error(
            message=f"course with ID {courseId} doee not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    course_to_be_removed = await Course_operations.delete_course(course)
    if course_to_be_removed:
        return True
    raise ErrorResponse.error(
        message=f"Error removing course with id {courseId}",
        status_code=status.WS_1011_INTERNAL_ERROR,
    )
