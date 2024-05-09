from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from config.database import Session
from models.books import Books as BookModel
from middlewares.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from models.categorias import Categorias as CategoryModel

category_router = APIRouter()

#Class libros y categorias
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

#Conseguir todas las categorias
@category_router.get('/categorias', tags=['categorias'], dependencies=[Depends(JWTBearer())])
def get_categorias() -> JSONResponse:
    db = Session()
    result = db.query(CategoryModel).all()
    if not result:
        return JSONResponse(status_code = 404, content={"message": "No se han agregado categorias"})
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#Crear categorias en la lista de categorias
@category_router.post('/categorias', tags=['categorias'], dependencies=[Depends(JWTBearer())])
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
@category_router.put('/categorias', tags=['categorias'], dependencies=[Depends(JWTBearer())])
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
@category_router.delete('/categorias', tags=['categorias'], dependencies=[Depends(JWTBearer())])
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