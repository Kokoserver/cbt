from backend.user.schema import User
from repository.authentication import get_current_user
from typing import Optional, Union
from fastapi import APIRouter, status
from fastapi import Depends
from .model import (
    CourseUpdate,
    Course as CourseModel,
    SemesterChoice,
    LevelChoice,
)
from .schema import Course
from backend.controller.courseCountrller import get, all, create, delete, update

router = APIRouter(prefix="/course", tags=["Course"])


@router.get(
    "/",
    response_model=Union[Course, list[Course]],
    status_code=status.HTTP_200_OK,
)
async def get_all_courses(
    courseId: Optional[str] = "",
    semester: Optional[SemesterChoice] = "",
    unit: Optional[int] = "",
    level: Optional[LevelChoice] = "",
) -> dict or list[dict]:
    if semester:
        course = await get(filterBy=semester, filterType="semester")
        return course
    if unit:
        course = await get(filterBy=int(unit), filterType="unit")
        return course
    if level:
        course = await get(filterBy=level, filterType="level")
        return course
    if courseId:
        course = await get(filterBy=courseId, filterType="id")
        return course
    all_course = await all()
    return all_course


@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
async def add_new_course(
    course: CourseModel,
    user: User = Depends(get_current_user),
):
    new_course = await create(course=course, user=user)
    return new_course


@router.put("/{courseId}", response_model=Course, status_code=status.HTTP_200_OK)
async def update_existing_course(
    course: CourseUpdate,
    courseId:str,
    user: User = Depends(get_current_user),
):
    course_update = await update(course=course, user=user, courseId=courseId)
    return course_update


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_course(
    courseId: str,
    user: User = Depends(get_current_user),
):
    course_update = await delete(courseId=courseId, user=user)
    if course_update:
        return True
