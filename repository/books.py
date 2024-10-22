from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.model import Book

async def create_book(db: AsyncSession, book_data: dict):
    book = Book(**book_data)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

async def get_book_by_id(db: AsyncSession, book_id: int):
    statement = select(Book).where(Book.id == book_id)
    result = await db.execute(statement)
    return result.scalars().first()

async def update_book(db: AsyncSession, book_id: int, book_data: dict):
    book = await get_book_by_id(db, book_id)
    if not book:
        return None
    for key, value in book_data.items():
        setattr(book, key, value)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

async def delete_book(db: AsyncSession, book_id: int):
    book = await get_book_by_id(db, book_id)
    if not book:
        return None
    await db.delete(book)
    await db.commit()
    return book
