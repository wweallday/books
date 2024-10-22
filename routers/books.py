from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository import book_repository
from dependencies import get_db

router = APIRouter()

@router.post("/books")
async def create_book(book_data: dict, db: AsyncSession = Depends(get_db)):
    book = await book_repository.create_book(db, book_data)
    return book

@router.get("/books/{book_id}")
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await book_repository.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}")
async def update_book(book_id: int, book_data: dict, db: AsyncSession = Depends(get_db)):
    updated_book = await book_repository.update_book(db, book_id, book_data)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/books/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted_book = await book_repository.delete_book(db, book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}
