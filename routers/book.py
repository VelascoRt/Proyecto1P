from fastapi import Body, Depends, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.books import Books as BookModel
from jwt_manager import create_token
from middlewares.jwt_bearer import JWTBerrer

book_router = APIRouter()

#User
class User(BaseModel):
    email:str
    password:str

#Login
@book_router.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "eds@gmail.com" and user.password == "Contraseña":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

#Class libros
class Libros(BaseModel):

    titulo: str =  Field(default = "Titulo del libro", min_length = 5, max_length=100)
    autor: str =  Field(default = "Autor del libro", min_length = 5, max_length=50)
    año: str =  Field(default = "2020", min_length = 1, max_length=4)
    categoria: str =  Field(default = "Categoria", min_length = 5, max_length=25)
    codigo: Optional[int] = None 
    numeroDePaginas: str =  Field(default = "100", min_length = 1, max_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "titulo":"Titulo del libro",
                "autor":"Autor del libro",
                "año":"2020",
                "categoria":"Categoria",
                "codigo": 0,
                "numeroDePaginas": "100"
            }
        }

#Categorias
categorias = []
#Libros
libros = []

#Mensaje de entrada
@book_router.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Libreria digital<h1>')

#Conseguir todos los libros
@book_router.get('/libreria', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBerrer())])
def get_libros() -> List[Libros]:
    return JSONResponse(status_code = 200, content=libros)

#Conseguir un libro por codigo
@book_router.get('/libreria/{codigo}', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBerrer())])
def get_libro(codigo: int) -> Libros:
    for item in libros:
        if item["codigo"] == codigo:
            return JSONResponse(status_code = 200, content=item)
    return JSONResponse(status_code = 404, content=[])

#Conseguir libros por categorias.
@book_router.get('/libreria/', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBerrer())])
def get_libros_by_categoria(categoria: str) -> List[Libros]:
   librosMarca = []
   for item in libros:
        if item["categoria"] == categoria:
            librosMarca.append(item) 
   if librosMarca == []:
       return JSONResponse(status_code = 404, content=librosMarca)
   return JSONResponse(status_code = 200, content=librosMarca)

#Crear libros en la lista de libros.
@book_router.post('/libros/', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBerrer())])
def create_libros(codigo: int = Body(), titulo: str = Body(), autor: str = Body(), año: str = Body(), categoria: str = Body(), numeroDePaginas: str = Body()) -> JSONResponse:
    for item in libros:
        if item["codigo"] == codigo:
            return JSONResponse(status_code = 409,content= {"message" : "El código ya está en uso."})
    for i in range(0,len(categorias)):
        if(categoria == categorias[i]):
            libros.append({
                "titulo":titulo,
                "autor": autor,
                "año": año,
                "categoria": categorias[i],
                "codigo": codigo,
                "numeroDePaginas" : numeroDePaginas
            })
            return JSONResponse(status_code=200,content= {"message" : "Se ha registrado el libro"})
    return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"}) 

#Actualizar libros.
@book_router.put('/libreria/{id}', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBerrer())]) 
def update_libros(codigo: int, titulo: str = Body(), autor: str = Body(), año: str = Body(), categoria: str = Body(), numeroDePaginas: str = Body()) -> JSONResponse: 
    for item in libros:
        if item["codigo"] == codigo:
            for i in range(0,len(categorias)):
                if( categoria == categorias[i]):
                    item["titulo"] = titulo
                    item["autor"] = autor
                    item["año"] = año
                    item["categoria"] = categorias[i]
                    item["numeroDePaginas"] = numeroDePaginas
                    return JSONResponse(status_code=200,content={"message:":"Se ha modificado el libro"})
            return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"})

#Eliminar libros de la lista de libros.
@book_router.delete('/libreria/{id}', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBerrer())])
def delete_libros(codigo: int) -> JSONResponse:
    for item in libros:
        if item["codigo"] == codigo:
            libros.remove(item)
            return JSONResponse(status_code= 200, content={"message:":"Se ha eliminado el libro exitosamente"}) 
    return JSONResponse(status_code=404, content={"message:":"No se ha encontrado el libro"})

#Conseguir todas las categorias
@book_router.get('/categorias', tags=['categorias'] , dependencies=[Depends(JWTBerrer())])
def get_categorias() -> JSONResponse:
    return JSONResponse(status_code = 200, content=categorias)

#Crear categorias en la lista de categorias
@book_router.post('/categorias', tags=['categorias'], dependencies=[Depends(JWTBerrer())])
def create_categorias(categoria:str) -> JSONResponse:
    for category in categorias:
        if category == categoria:
            return JSONResponse(status_code=409, content={"message" : "La categoria ya existe."})
    categorias.append(categoria)
    return JSONResponse(status_code=200, content={"message" : "Se ha registrado la categoria " + categoria + " en la lista."})

#Actualizar categorias de la lista de categorias.
@book_router.put('/categorias', tags=['categorias'], dependencies=[Depends(JWTBerrer())])
def update_categorias(viejaCategoria:str, nuevaCategoria:str) -> JSONResponse:
    for i in range(0,len(categorias)):
        if categorias[i] == viejaCategoria:
            categorias[i] = nuevaCategoria
            for item in libros:
                if (item["categoria"] == viejaCategoria):
                    item["categoria"] = nuevaCategoria
            return JSONResponse(status_code=200, content={"message" : "La categoria se ha modificado exitosamente"})
    return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"})

#Eliminar categorias de la lista de categorias
@book_router.delete('/categorias', tags=['categorias'], dependencies=[Depends(JWTBerrer())])
def delete_categorias(categoria:str) -> JSONResponse:
    for i in range(0,len(categorias)):
        if categoria == categorias[i]:
            for item in libros:
                if item["categoria"] == categoria:
                    return JSONResponse(status_code = 409,content={"message:":"La categoria está siendo usada"})
            categorias.remove(categorias[i])
            return JSONResponse(status_code=200, content={"message" : "La categoria se ha eliminado exitosamente"}) 
    return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"})    
