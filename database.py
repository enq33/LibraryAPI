from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///library.db"

engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(MappedAsDataclass, DeclarativeBase):
    pass


async def get_session():
    async with new_session() as session:
        yield session
