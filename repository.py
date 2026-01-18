from sqlalchemy.ext.asyncio import AsyncSession
from models.books import BooksModel
from schemas.books import SBookAdd
from sqlalchemy import select


class BookRepository:
    @classmethod
    async def add_book(cls, session: AsyncSession, data: SBookAdd):
        """
        Добавляет новую книгу в базу данных.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            data (SBookAdd): Данные книги от клиента.

        Returns:
            BooksModel: ORM-объект добавленной книги с заполненным id и
            дефолтными полями.
        """
        book_dict = data.model_dump()
        book = BooksModel(**book_dict)

        session.add(book)
        await session.commit()
        await session.refresh(book)

        return book

    @classmethod
    async def get_all_books(cls, session: AsyncSession):
        """
        Возвращает список всех книг из базы данных.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.

        Returns:
            list[BooksModel]: Список объектов книг.
        """
        query = select(BooksModel)
        result = await session.execute(query)
        book_models = result.scalars().all()

        return book_models

    @classmethod
    async def get_book_by_id(cls, session: AsyncSession, book_id: int):
        """
        Находит книгу по её ID.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            book_id (int): ID искомой книги.

        Returns:
            BooksModel | None: Объект книги, если найден, иначе None.
        """
        query = select(BooksModel).where(BooksModel.id == book_id)
        result = await session.execute(query)
        book_model = result.scalars().first()

        return book_model

    @classmethod
    async def update_book(
        cls,
        session: AsyncSession,
        book_id: int,
        data: SBookAdd
    ):
        """
        Обновляет данные существующей книги.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            book_id (int): ID книги для обновления.
            data (SBookAdd): Новые данные книги.

        Returns:
            BooksModel | None: Обновлённый объект книги.
        """
        book = await BookRepository.get_book_by_id(session, book_id)
        if book is None:
            return

        book.title = data.title
        book.author = data.author
        book.year = data.year
        book.pages = data.pages
        book.is_read = data.is_read

        await session.commit()

        return

    @classmethod
    async def delete_book(cls, session: AsyncSession, book_id: int):
        """
        Удаляет книгу из базы данных по её ID.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
            book_id (int): ID книги для удаления.

        Returns:
            None
        """
        book = await BookRepository.get_book_by_id(session, book_id)
        if book is None:
            return

        await session.delete(book)
        await session.commit()

        return
