import uvicorn
from fastapi import FastAPI, Body, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Biblioteca digital"
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

libros = [
    {
    "titulo":"El cuervo",
    "autor": "Edgar Allan Poe",
    "año": "1948",
    "categoria": "Drama",
    "codigo": 0,
    "numeroDePaginas" : "500"

},
{
    "titulo":"Persona normal",
    "autor": "Benito Taibo",
    "año": "2011",
    "categoria": "Ficcion",
    "codigo": 1,
    "numeroDePaginas" : "248"

}
]

@app.get('/', tags = ['home'])

def message():
    return HTMLResponse('<h1>Libreria digital<h1>')

@app.get('/libreria', tags=['libreria'], response_model=List[Libros])
def get_libros() -> List[Libros]:
    return JSONResponse(status_code = 200, content=libros)

@app.get('/libreria/{id}', tags=['libreria'], response_model=List[Libros])
def get_libro(codigo: int) -> Libros:
    for item in libros:
        if item["codigo"] == codigo:
            return JSONResponse(status_code= 404, content=item)
    return[]

@app.get('/libreria/', tags=['libreria'], response_model=List[Libros])
def get_libros_by_categoria(categoria: str):
   librosMarca = []
   for item in libros:
        if item["categoria"] == categoria:
            librosMarca.append(item) 
   return JSONResponse(content=librosMarca)

@app.delete('/libreria/{id}', tags=['libreria'], response_model=List[Libros])
def delete_libros(codigo: int):
     for item in libros:
        if item["codigo"] == codigo:
            libros.remove(item)
            return JSONResponse(status_code= 404, content=item)