from re import template
from fastapi.param_functions import Depends
from odmantic.bson import ObjectId
from starlette.responses import Response
from backend.user.schema import User
from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from repository.context import context as question_context
from repository.authentication import get_current_user
from repository.db_operations.find_question import Question_operations
router = APIRouter(prefix="/question")


@router.get("/{limit}/{skip}")
async def all_question(request:Request, user:User = Depends(get_current_user), limit:int = 10, skip:int = 10, sort:str = None, q:str = None,  message:str = None, error:str = ""):
     if user.is_admin:
          all_questions = Question_operations.all_questions(limit, skip, sort)
          if all_questions:
               return template("/question", question_context(request, {"question":all_questions, "message":message}))
          return template("/compoents/question/allQuestion.html", question_context(request, data={"questions":[], "message":message, "error":error}))
     return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
     

@router.get("/{questionId}")
async def single_question(request:Request, questionId:str, user:User = Depends(get_current_user)):
     if user.is_admin:
           question = await Question_operations.find_question_by_ID(id=ObjectId(questionId))
           if questionId:
               return template("/comonents/question/details.html", question_context(request, {"questions":question}))
           return RedirectResponse(request.url_for("/question"))
     return RedirectResponse(request.url_for("/"))

@router.get("/register")
async def add_question(request:Request):
     context = question_context()
     pass

@router.post("/register", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def add_question(request:Request):
     context = question_context()
     pass

@router.get("/update/{questionId}")
async def update_question(request:Request, questionId:str):
     context = question_context({"question":"", "questionId":questionId})
     #TODO pass the questionId as a context
     pass

@router.post("/update", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def update_question(request:Request):
     pass

@router.get("/remove/{questionId}", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def remove_question(request:Request):
     pass

