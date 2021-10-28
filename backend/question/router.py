from backend.course.model import CourseUnitChoice
from backend.user.schema import User
from repository.authentication import get_current_user
from typing import Optional, Union
from fastapi import APIRouter, status
from fastapi import Depends
from backend.course.model import LevelChoice, SemesterChoice
from .schema import Question as QuestionSchema
from .model import (
   QuestionUpdate,
   Question as QuestionModel,
)

from backend.controller.questionController import get, all, create, delete, update

router = APIRouter(prefix="/question", tags=["Question"])

@router.get(
    "/",
    response_model=Union[QuestionSchema, list[QuestionSchema]],
    status_code=status.HTTP_200_OK,
)
async def get_all_questions(
    QuestionId: Optional[str] = "",
    semester: Optional[SemesterChoice] = "",
    unit: Optional[CourseUnitChoice] = "",
    level: Optional[LevelChoice] = ""
) -> dict or list[dict]:
    if semester:
        question = await get(filterBy=semester, filterType="semester")
        return question
    if unit:
        question = await get(filterBy=int(unit), filterType="unit")
        return question
    if level:
        question = await get(filterBy=level, filterType="level")
        return question
    if QuestionId:
        question = await get(filterBy=QuestionId, filterType="id")
        return question
    all_question = await all()
    return all_question


@router.post("/", response_model=QuestionSchema, status_code=status.HTTP_201_CREATED)
async def add_new_question(
    question: QuestionModel,
    user: User = Depends(get_current_user),
):
    new_question = await create(question=question, user=user)
    return new_question


@router.put("/{questionId}", response_model=QuestionSchema, status_code=status.HTTP_200_OK)
async def update_existing_question(
    questionId:str,
    question: QuestionUpdate,
    user: User = Depends(get_current_user),
):
    question_update = await update(question=question, user=user, questionId=questionId)
    return question_update


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_question(
    questionId: str,
    user: User = Depends(get_current_user),
):
    question_update = await delete(questionId=questionId, user=user)
    if question_update:
        return True
