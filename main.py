from fastapi import FastAPI,Body, Depends
from middlewares.error_handler import ErrorHandler
from routers.book import book_router
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.books import Books as BookModel
from models.categorias import Categorias as CategoryModel
from middlewares.jwt_bearer import JWTBearer
from jwt_manager import create_token
from fastapi.encoders import jsonable_encoder

from config.database import engine, Base

app = FastAPI()
app.title = "Biblioteca digital"

# app.add_middleware(ErrorHandler)
# app.include_router(book_router)

Base.metadata.create_all(bind=engine)
class Categorias(BaseModel):
    id: Optional[int] = None
    name: str = Field(default= "Ficcion", min_length=2, max_length=200)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id":"0",
                "name":"Ficcion",
            }
        }

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

categorias = []

libros = []

#User
class User(BaseModel):
    email:str
    password:str

#Login
@app.post('/login', tags = ['auth'])
def login(user: User):
    if user.email == "eds@gmail.com" and user.password == "pass":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else: 
        return JSONResponse(status_code=403, detail="Credenciales invalidas.")


#Mensaje de entrada
@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Libreria digital<h1>')

#Conseguir todos los libros
@app.get('/libreria', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())])
def get_libros() -> JSONResponse:
    db = Session()
    result = db.query(BookModel).all()
    return JSONResponse(status_code = 200, content= jsonable_encoder(result))

#Conseguir un libro por codigo
@app.get('/libreria/{codigo}', tags=['libreria'], response_model=List[Libros],dependencies=[Depends(JWTBearer())])
def get_libro(codigo: int) -> JSONResponse:
    db = Session()
    result = db.query(BookModel).filter(BookModel.codigo == codigo).first()
    if not result:
        return JSONResponse(status_code = 404, content={"message": "No encontrado"})
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#Conseguir libros por categorias.
@app.get('/libreria/', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())])
def get_libros_by_categoria(categoria: str) -> JSONResponse:
   db = Session()
   result = db.query(BookModel).filter(BookModel.categoria == categoria).all()
   if not result:
        return JSONResponse(status_code = 404, content={"message": "No hay libros con esa categoria"})
   return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#Crear libros en la lista de libros.
@app.post('/libros/', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())])
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
@app.put('/libreria/{id}', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())]) 
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
@app.delete('/libreria/{id}', tags=['libreria'], response_model=List[Libros], dependencies=[Depends(JWTBearer())])
def delete_libros(codigo: int) -> JSONResponse:
    db = Session()
    result = db.query(BookModel).filter(BookModel.codigo == codigo).first()
    if not result:
        return JSONResponse(status_code = 404, content={"message": "No encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code= 200, content={"message:":"Se ha eliminado el libro exitosamente"}) 

#Conseguir todas las categorias
@app.get('/categorias', tags=['categorias'], dependencies=[Depends(JWTBearer())])
def get_categorias() -> JSONResponse:
    db = Session()
    result = db.query(CategoryModel).all()
    if not result:
        return JSONResponse(status_code = 404, content={"message": "No se han agregado categorias"})
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#Crear categorias en la lista de categorias
@app.post('/categorias', tags=['categorias'], dependencies=[Depends(JWTBearer())])
def create_categorias(categoria:Categorias) -> JSONResponse:
    db = Session()
    new_categoria = CategoryModel(** categoria.model_dump())
    result = db.query(CategoryModel).filter(CategoryModel.name == categoria.name).first()
    if not result:
        db.add(new_categoria)
        db.commit()
        return JSONResponse(status_code=200, content={"message" : "Se ha registrado la categoria "})
    return JSONResponse(status_code=409, content={"message" : "La categoria ya existe."})
    
    
#Actualizar categorias de la lista de categorias.
@app.put('/categorias', tags=['categorias'], dependencies=[Depends(JWTBearer())])
def update_categorias(id:int, category:Categorias) -> JSONResponse:
    db = Session()
    result = db.query(CategoryModel).filter(CategoryModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"})
    cat = db.query(CategoryModel).filter(CategoryModel.name == category.name).first()
    if not not cat:
        return JSONResponse(status_code=409, content={"message" : "La categoria ya existe."})
    catUso = db.query(BookModel).filter(BookModel.categoria == result.name).all()
    for cats in catUso:
        cats.categoria = category.name
    result.name = category.name
    db.commit()
    return JSONResponse(status_code=200, content={"message" : "La categoria se ha modificado exitosamente"})

#Eliminar categorias de la lista de categorias
@app.delete('/categorias', tags=['categorias'], dependencies=[Depends(JWTBearer())])
def delete_categorias(Categoria:str) -> JSONResponse:
    db = Session()
    result = db.query(CategoryModel).filter(CategoryModel.name == Categoria).first()
    if not result:
        return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"})
    cat = db.query(BookModel).filter(BookModel.categoria == result.name).first()
    if not not cat:
        return JSONResponse(status_code=409, content={"message" : "La categoria ya está en uso."})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message" : "La categoria se ha eliminado exitosamente"})  