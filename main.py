from fastapi import FastAPI
from middlewares.error_handler import ErrorHandler
from routers.book import book_router
from routers.category import category_router
from routers.user import user_router

from config.database import engine, Base

app = FastAPI()
app.title = "Biblioteca digital"

app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(book_router)
app.include_router(category_router)


Base.metadata.create_all(bind=engine)
