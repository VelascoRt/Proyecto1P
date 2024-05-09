from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token

user_router = APIRouter()

#User
class User(BaseModel):
    email:str
    password:str

#Login
@user_router.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "eds@gmail.com" and user.password == "pass":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else: 
        return JSONResponse(status_code=403, detail="Credenciales invalidas.")
