from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from repository.context import context as course_context
router = APIRouter(prefix="/course")


@router.get("/{limit}/{skip}")
async def all_course(request:Request, limit:int = 10, skip:int = 10, q:str = None, message:str = None):
     context = course_context({"course":"", "message":message})
     pass

@router.get("/{courseId}")
async def all_course(request:Request, courseId:str):
     context = course_context({"course":""})
     pass

@router.get("/register")
async def add_course(request:Request):
     context = course_context()
     pass

@router.post("/register", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def add_course(request:Request):
     context = course_context()
     pass

@router.get("/update/{courseId}")
async def register(request:Request, courseId:str):
     context = course_context({"course":"", "courseId":courseId})
     #TODO pass the courseId as a context
     pass

@router.post("/update", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def register(request:Request):
     pass

@router.get("/remove/{courseId}", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def forgotpassword(request:Request):
     pass

