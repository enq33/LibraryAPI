from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.books import SBookAdd, SBook
from repository import BookRepository
from database import get_session

router = APIRouter(prefix="/books", tags=["Книги"])


@router.post("/", response_model=SBook,
             status_code=status.HTTP_201_CREATED)
async def add_book(
    data: SBookAdd,
    session: AsyncSession = Depends(get_session)
):
    """Добавить книгу"""
    book = await BookRepository.add_book(session, data)

    return book


@router.get("/", response_model=list[SBook],
            status_code=status.HTTP_200_OK)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    """Получить список всех книг"""
    books = await BookRepository.get_all_books(session)
    return books


@router.get("/{book_id}", response_model=SBook,
            status_code=status.HTTP_200_OK)
async def get_book_by_id(
    book_id: int,
    session: AsyncSession = Depends(get_session),
):
    """Получить книгу по ID"""
    book = await BookRepository.get_book_by_id(session, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")
    return book


@router.put("/{book_id}", response_model=SBook,
            status_code=status.HTTP_200_OK)
async def update_book(
    book_id: int,
    data: SBookAdd,
    session: AsyncSession = Depends(get_session)
):
    """Обновить книгу"""
    book = await BookRepository.update_book(session, book_id, data)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Удалить книгу"""
    # Проверка на наличие книги
    book = await BookRepository.get_book_by_id(session, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Book not found")

    # Удаление книги
    await BookRepository.delete_book(session, book_id)
    return
