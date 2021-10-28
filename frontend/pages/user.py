from frontend.form.userupdateForm import UpdateForm
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from backend.user.schema import User
from fastapi.responses import Response
from fastapi import APIRouter, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from repository.context import context as user_context
from repository.authentication import   get_current_user
from repository.db_operations.find_user import User_operations
from repository.password_hasher import Hasher
from frontend.form.registerForm import RegisterForm
from frontend.form.loginForm import LoginForm
from backend.user.router import Login_User_OpenApi
from jose import JWTError
from main import template

router = APIRouter(prefix="/user")

@router.get("/", name="all_user")
async def all_user(request:Request,  user:User = Depends(get_current_user), skip:Optional[int] = 0, q:str = None, message:str = None, error:str = None,):
     if user.is_admin:
          users = await User_operations.get_all_user(skip=int(skip))
          if users:
               return template("components/user/allUser.html",user_context(
                    request, {"users":users, "message":message, "error":error}))
          return template("components/user/allUser.html", user_context(request, {"users":[], "message":message, "error":error}))
     return template("index.html",user_context(request=request))


@router.get("/{userId}/details", name="single_user")
async def single_user(request:Request,  userId:str,  user:User = Depends(get_current_user)):
     if not user.is_admin:
          return RedirectResponse(url="/users/?message=user does not=exist", status_code=status.HTTP_302_FOUND)
     check_user = User_operations.find_user_by_ID(user_id=userId)
     if check_user:
          return template("components/user/details.html", user_context(request=request, data={"users":user, "errors":{}}))
     return RedirectResponse(request.url_for("index"))


@router.get("/login", name="user_login_page")
async def login_user(request:Request, message:str = "", error:str = ""):
     return template("components/user/login.html", {"request":request, "errors":{}, "user":{},"message":message, "error":error})


@router.post("/login", name="user_login", status_code=status.HTTP_302_FOUND)
async def login_user(request:Request):
   try:
     form = LoginForm(request=request)
     _ = await form.load()
     form_validate = await form.is_valid()
     if not form_validate:
          return template("components/user/login.html", {"request":request, "errors":form.errors, "user":form.__dict__})
     check_user:User = await User_operations.find_user_by_Email(email=form.email)
     if not check_user:
          form.errors.update({"email":"Account does not exist"})
          return template("components/user/login.html", {"request":request, "errors":form.errors, "user":form.__dict__})
   
     response =  RedirectResponse("/?message=login successful", status_code=status.HTTP_302_FOUND)
     _ =  await Login_User_OpenApi(response=response, userForm=form)
     return response
   except JWTError:
        return template("components/user/login.html", {"request":request, "errors":{}, "user":form.__dict__, "password":" Incorrect password "})
   except HTTPException as e:
         return template("components/user/login.html", {"request":request, "errors":{}, "user":form.__dict__, "error":"please make sure you account is activated and try again"})
   except Exception as e:
         return template("components/user/login.html", {"request":request, "errors":{}, "user":form.__dict__, "error":"error login "})
        


     
     
@router.get("/register", name="user_register_page")
async def add_user(request:Request):
     return template("components/user/register.html", user_context(request, data={"errors":{}, "user":{}}) )

@router.post("/register",  name="user_register")
async def add_user(request:Request):
     form = RegisterForm(request = request)
     _ = await form.load()
     validate_form = await form.is_valid()
     if not validate_form:
          return template("components/user/register.html", user_context(request, data={"errors":form.errors,"user":form.__dict__}))
     check_user = await User_operations.find_user_by_Email(email=form.email)
     if check_user:
          return template("components/user/register.html", user_context(request, data={"errors":{"email":"user with this email already exist"},"user":form.__dict__}))
     password_hashed = Hasher.hash_password(plain_password=form.password)
     form.password = password_hashed
     if password_hashed:
          user = User(**form.__dict__)
          new_user = await User_operations.save_user(user)
          if new_user:
               return RedirectResponse( "/user/login?message=account was created succesffuly", status_code=status.HTTP_302_FOUND)
     return RedirectResponse("/?error=error creating account", status_code=status.HTTP_302_FOUND)

@router.post("/update",  name="user_register")
async def add_user(request:Request):
     form =UpdateForm(request = request)
     _ = await form.load()
     validate_form = await form.is_valid()
     if not validate_form:
          return RedirectResponse( "/user", status_code=status.HTTP_302_FOUND)
     check_user = await User_operations.find_user_by_ID(user_id=form.id)
     if check_user:
          update_user:dict = check_user
          update_user = form.__dict__
          update_user.update({"password":check_user.password})
          update_user = await User_operations.save_user(update_user)
     return RedirectResponse( f"/user/{check_user.id}/details", status_code=status.HTTP_302_FOUND) 




@router.get("/activate/{userId}", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def add_user(request:Request, userId:str):
     context = user_context(request=request)
     user = await User_operations.find_user_by_ID(user_id=userId)
     if user:
          user.is_active = True
          User_operations.save_user(user)
     return "/user/login?message=account was activated succesfully"


@router.get("/forget/password")
async def update_password(request:Request):
     context = user_context(request)
     return template("components/user/fogotpassword.html", context)

@router.post("/forget/password", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def update_password(request:Request):
     form = await request.form()
     email= form.get("email")
     if not email:
          return template("components/users/fogotpassword.html", user_context(request, data={"errors":{"email":"Please provide your email"}, "email":email}) )
     user = await User_operations.find_user_by_Email(email=email)
     if not user:
          return template("components/users/fogotpassword.html", user_context(request, data={"errors":{"email":"Account does not exist"}, "email":email }))
     #TODO send email to user account
     return "/?message=password reset link has been sent to your email"

@router.get("/forget/password/{userId}")
async def update_password(request:Request, userId:str):
     context = user_context(request,data={"userId":userId, "errors":{}})
     return template("components/user/passwordReset.html", context )

@router.post("/forget/password/{userId}", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def update_password(request:Request, userId:str):
     form = await request.form()
     password, conformPassword  = form.get("password"), form.get("confirmPawword")
     if password != conformPassword:
          return template("components/user/passwordReset.html", user_context(request, data={"errors":{"conformassword":"password do not match"}}))
     user:User = await User_operations.find_user_by_ID(user_id=userId)
     if not user:
          return "/user/login?error=user does not exist"
     password = Hasher.hash_password(plain_password=password)
     if password:
        user.password = password
        user = await User_operations.save_user(user)
        return "/user/login?message=password reset succesffuly"
     return "/user/login?message=error reseting user password"
     

@router.get("/remove/{userId}", name="remove_user", response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
async def forgotpassword(userId:str, request:Request,  user:User = Depends(get_current_user)):
     if not user.is_admin:
          return request.url_for("/")
     user = await User_operations.find_user_by_ID(user_id=userId)
     if user:
          remove_user = await User_operations.delete_user(user)
          if remove_user:
              return "/user"
     return "/user"



