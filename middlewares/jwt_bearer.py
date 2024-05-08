from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_manager import validate_token

class JWTBerrer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if (data['email'] != "victor7044@gmail.com"):
            raise HTTPException(status_code=403, detail="Credenciales invalidas.")