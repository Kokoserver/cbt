from backend.user.schema import User
from fastapi import status
from odmantic.bson import ObjectId
from backend.question.schema import Question
from backend.question.model import Question as QuestionModel, QuestionUpdate, SaveQuestion
from repository.db_operations.find_question import Question_operations
from repository.errors import ErrorResponse


async def all():
    all_questions = await Question_operations.get_all_question()
    if all_questions:
        return all_questions
    return []


async def get(filterBy: str, filterType: str):
    question = await Question_operations.filter_question(
        filterBy=filterBy, filterType=filterType
    )
    if question:
        return question
    raise ErrorResponse.error(
        message=f"question with {filterBy} doee not exist",
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def create(question:QuestionModel, user: User):
    if not user.is_admin:
        raise ErrorResponse.error(
            message=f" Only admin can perform this operation",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if not question.answer in question.options:
         raise ErrorResponse.error(
            message=f"Answer must be part of the options provided",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    check_question = await Question_operations.find_question_by_either(find_by=question)
    if check_question:
        raise ErrorResponse.error(
            message=f"question with either {question.question}, {question.answer} , already  exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    question_to_be_saved = Question(**question.dict())
    new_question = await Question_operations.save_question(question_to_be_saved)
    if new_question:
        return new_question
    raise ErrorResponse.error(
        message="Error savings this question", status_code=status.WS_1011_INTERNAL_ERROR
    )


async def update(question: QuestionUpdate, user: User, questionId:str):
    if not user.is_admin:
        raise ErrorResponse.error(
            message=f" Only admin can perform this operation",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if not question.answer in question.options:
         raise ErrorResponse.error(
            message=f"Answer must be part of the options provided",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    get_question = await Question_operations.find_question_by_ID(id=ObjectId(questionId))
    if not get_question:
        raise ErrorResponse.error(
            message=f"question with ID '{questionId}' doee not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    check_question = SaveQuestion(**question.dict(), id=questionId)
    if check_question == get_question:
         raise ErrorResponse.error(
            message=f"question already exist, please updated it and try again",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    get_question = check_question
    new_question = await Question_operations.save_question(get_question)
    if new_question:
        return new_question
    raise ErrorResponse.error(
        message=f"Error updating this question", status_code=status.WS_1011_INTERNAL_ERROR
    )

async def delete(questionId: str, user: User):
    if not user.is_admin:
        raise ErrorResponse.error(
            message=f" Only admin can perform this operation",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    question = await Question_operations.find_question_by_ID(id=ObjectId(questionId))
    if not question:
        raise ErrorResponse.error(
            message=f"question with ID {questionId} doee not exist",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    question_to_be_removed = await Question_operations.delete_question(question)
    if question_to_be_removed:
        return True
    raise ErrorResponse.error(
        message=f"Error removing question with id {questionId}",
        status_code=status.WS_1011_INTERNAL_ERROR,
    )
