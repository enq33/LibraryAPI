from fastapi import FastAPI
from database import Model, engine
from routers.books import router as books_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- КОД ПРИ СТАРТЕ ---
    # Мы обращаемся к движку и просим создать все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    print("База данных готова к работе")

    yield  # Разделяет старт и выключение

    # --- КОД ПРИ ВЫКЛЮЧЕНИИ ---
    print("Выключение сервера")

app = FastAPI(
    lifespan=lifespan,
    title="LibraryAPI",
    description="API для управления библиотекой книг",
    version="0.1.0"
)

app.include_router(books_router)
