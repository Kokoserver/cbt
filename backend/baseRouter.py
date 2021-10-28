from fastapi import APIRouter
from backend.user.router import router as user_router
from backend.question.router import router as questiom_router
from backend.course.router import router as course_router
backendRouter = APIRouter()
backendRouter.include_router(router=user_router)
backendRouter.include_router(router=questiom_router)
backendRouter.include_router(router=course_router)

