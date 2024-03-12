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

categorias = ["Novela","Poesia","Cuento","Ensayo","Drama","Ciencia ficcion", "Fantasia",
              "Misterio","Romance","Terror","Aventura","Historia","Biografia","Autoayuda",
              "Politica","Filosofia","Economia","Ciencia","Psicologia","Religion","Educacion",
              "Cocina","Musica","Entretenimiento", "Ficcion"]

libros = [
    {
    "titulo":"El cuervo",
    "autor": "Edgar Allan Poe",
    "año": "1948",
    "categoria": categorias[4],
    "codigo": 0,
    "numeroDePaginas" : "500"

},
{
    "titulo":"Persona normal",
    "autor": "Benito Taibo",
    "año": "2011",
    "categoria": categorias[24],
    "codigo": 1,
    "numeroDePaginas" : "248"

}
]

#Mensaje de entrada
@app.get('/', tags = ['home'])
def message():
    return HTMLResponse('<h1>Libreria digital<h1>')

#Conseguir todos los libros
@app.get('/libreria', tags=['libreria'], response_model=List[Libros])
def get_libros() -> List[Libros]:
    return JSONResponse(status_code = 200, content=libros)

#Conseguir un libro por codigo
@app.get('/libreria/{codigo}', tags=['libreria'], response_model=List[Libros])
def get_libro(codigo: int) -> Libros:
    for item in libros:
        if item["codigo"] == codigo:
            return JSONResponse(status_code = 200, content=item)
    return JSONResponse(status_code = 404, content=[])

#Conseguir libros por categorias.
@app.get('/libreria/', tags=['libreria'], response_model=List[Libros])
def get_libros_by_categoria(categoria: str):
   librosMarca = []
   for item in libros:
        if item["categoria"] == categoria:
            librosMarca.append(item) 
   if librosMarca == []:
       return JSONResponse(status_code = 404, content=librosMarca)
   return JSONResponse(status_code = 200, content=librosMarca)

#Crear libros en la lista de libros.
@app.post('/libros/', tags=['libreria'], response_model=List[Libros])
def create_libros(codigo: int = Body(), titulo: str = Body(), autor: str = Body(), año: str = Body(), categoria: str = Body(), numeroDePaginas: str = Body()):
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
            return JSONResponse(status_code=200,content= {"message" : "Se ha registrado la pelicula"})
    return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"}) 

#Actualizar libros.
@app.put('/libreria/{id}', tags=['libreria'], response_model=List[Libros]) 
def update_libros(codigo: int, titulo: str = Body(), autor: str = Body(), año: str = Body(), categoria: str = Body(), numeroDePaginas: str = Body()) -> dict: 
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
@app.delete('/libreria/{id}', tags=['libreria'], response_model=List[Libros])
def delete_libros(codigo: int):
    for item in libros:
        if item["codigo"] == codigo:
            libros.remove(item)
            return JSONResponse(status_code= 200, content={"message:":"Se ha eliminado el libro exitosamente"}) 
    return JSONResponse(status_code=404, content={"message:":"No se ha encontrado el libro"})

#Conseguir todas las categorias
@app.get('/categorias', tags=['categorias'])
def get_categorias():
    return JSONResponse(status_code = 200, content=categorias)

#Crear categorias en la lista de categorias
@app.post('/categorias', tags=['categorias'])
def create_categorias(categoria:str):
    for category in categorias:
        if category == categoria:
            return JSONResponse(status_code=409, content={"message" : "La categoria ya existe."})
    categorias.append(categoria)
    return JSONResponse(status_code=200, content={"message" : "Se ha registrado la categoria " + categoria + " en la lista."})

#Actualizar categorias de la lista de categorias.
@app.put('/categorias', tags=['categorias'])
def update_categorias(viejaCategoria:str, nuevaCategoria:str):
    for i in range(0,len(categorias)):
        if categorias[i] == viejaCategoria:
            categorias[i] = nuevaCategoria
            for item in libros:
                if (item["categoria"] == viejaCategoria):
                    item["categoria"] = nuevaCategoria
            return JSONResponse(status_code=200, content={"message" : "La categoria se ha modificado exitosamente"})
    return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"})

#Eliminar categorias de la lista de categorias
@app.delete('/categorias', tags=['categorias'])
def delete_categorias(categoria:str):
    for i in range(0,len(categorias)):
        if categoria == categorias[i]:
            for item in libros:
                if item["categoria"] == categoria:
                    return JSONResponse(status_code = 409,content={"message:":"La categoria está siendo usada"})
            categorias.remove(categorias[i])
            return JSONResponse(status_code=200, content={"message" : "La categoria se ha eliminado exitosamente"}) 
    return JSONResponse(status_code = 404,content={"message:":"La categoria no existe"})    