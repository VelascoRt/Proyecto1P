from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.books import Books as BookModel
from middlewares.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from jwt_manager import create_token
from models.categorias import Categorias as CategoryModel

book_router = APIRouter()

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
#Mensaje de entrada
@book_router.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Libreria digital<h1>')

#Conseguir todos los libros
@book_router.get('/libreria', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())])
def get_libros() -> JSONResponse:
    db = Session()
    result = db.query(BookModel).all()
    return JSONResponse(status_code = 200, content= jsonable_encoder(result))

#Conseguir un libro por codigo
@book_router.get('/libreria/{codigo}', tags=['libreria'], response_model=List[Libros],dependencies=[Depends(JWTBearer())])
def get_libro(codigo: int) -> JSONResponse:
    db = Session()
    result = db.query(BookModel).filter(BookModel.codigo == codigo).first()
    if not result:
        return JSONResponse(status_code = 404, content={"message": "No encontrado"})
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#Conseguir libros por categorias.
@book_router.get('/libreria/', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())])
def get_libros_by_categoria(categoria: str) -> JSONResponse:
   db = Session()
   result = db.query(BookModel).filter(BookModel.categoria == categoria).all()
   if not result:
        return JSONResponse(status_code = 404, content={"message": "No hay libros con esa categoria"})
   return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#Crear libros en la lista de libros.
@book_router.post('/libros/', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())])
def create_libros(Book: Libros) -> JSONResponse:
    db = Session()
    new_book = BookModel(** Book.model_dump())
    book = db.query(BookModel).filter(BookModel.codigo == new_book.codigo).first()
    if not not book:
        return JSONResponse(status_code = 409,content= {"message" : "El código ya está en uso."})
    cat = db.query(CategoryModel).filter(CategoryModel.name == new_book.categoria).first()
    if not cat:
        return JSONResponse(status_code = 409,content= {"message" : "La categoría no existe"})
    db.add(new_book)
    db.commit()
    return JSONResponse(status_code=200, content= {"message" : "El libro se ha creado"})
    

#Actualizar libros.
@book_router.put('/libreria/{id}', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())]) 
def update_libros(Book : Libros, codigo : int) -> JSONResponse: 
    db = Session()
    result = db.query(BookModel).filter(BookModel.codigo == codigo).first()
    if not result:
        return JSONResponse(status_code = 404, content={"message": "No encontrado"})
    cat = db.query(CategoryModel).filter(CategoryModel.name == Book.categoria).first()
    if not cat:
        return JSONResponse(status_code = 409,content= {"message" : "La categoría no existe"})
    result.titulo = Book.titulo
    result.autor = Book.autor
    result.categoria = Book.categoria
    result.numeroDePaginas = Book.numeroDePaginas
    result.año = Book.año
    db.commit()
    return JSONResponse(status_code=200,content={"message:":"Se ha modificado el libro"})

#Eliminar libros de la lista de libros.
@book_router.delete('/libreria/{id}', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())])
def delete_libros(codigo: int) -> JSONResponse:
    db = Session()
    result = db.query(BookModel).filter(BookModel.codigo == codigo).first()
    if not result:
        return JSONResponse(status_code = 404, content={"message": "No encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code= 200, content={"message:":"Se ha eliminado el libro exitosamente"}) 