from fastapi import APIRouter
from fastapi.param_functions import Cookie
from starlette.requests import Request
from main import template
from frontend.pages.course import router as courseRouter
from frontend.pages.question import router as questionRouter
from frontend.pages.user import router as userRouter
from repository.context import context
router = APIRouter(include_in_schema=False)
router.include_router(router=courseRouter, tags=["course route"])
router.include_router(router=userRouter, tags=["user route"])
router.include_router(router=questionRouter , tags=["question route"])

@router.get("/", include_in_schema=False, status_code=200, name="index")
def index_page(request:Request, message:str = None):
    return template("index.html",context(data={"message":message}, request=request) )
