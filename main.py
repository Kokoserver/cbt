from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# Linking the template url for html files
template = Jinja2Templates("./frontend/template/").TemplateResponse

# routers
from backend.baseRouter import backendRouter
from frontend.frontendBaseRouter import router as frontendRouter


# Initializing fastapi
app = FastAPI()
# adding missleware to fastapi
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
    ],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mouting static files directory to fastapi
app.mount("/static", StaticFiles(directory="./frontend/static"), name="static")
# default routes
app.include_router(router=backendRouter, prefix="/api")
app.include_router(router=frontendRouter, include_in_schema=False)

