from os import getenv
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from pydantic import BaseModel
from starlette import requests

class User(BaseModel):
    username: str
    password: str

# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = getenv("SECRET_KEY", "")
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_secure: bool = bool(getenv("DEBUG"))
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    # authjwt_cookie_samesite: str = 'lax'

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

# routers
from backend.routes.userRoute import router as userRoutes
from backend.routes.examRoute import router as examRout
from repository.utils import validation_bad_request_exception_handler


# Initializing fastapi
app = FastAPI(
    exception_handlers={
        RequestValidationError: validation_bad_request_exception_handler
    }
)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: requests, exc: AuthJWTException):
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )


# adding missleware to fastapi
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["PATCH", "GET", "PUT", "POST", "DELETE"],
    allow_headers=["*"],
)


# including routes
app.include_router(router=userRoutes, prefix="/api/user")
app.include_router(router=examRout, prefix="/api/exam")
