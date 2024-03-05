import uvicorn
from fastapi import FastAPI, Body, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Biblioteca digital"

libros = {
    
}

