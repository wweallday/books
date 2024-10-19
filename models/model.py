from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import date
from models.schema import BookType

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password_hash: str
    purchase_history: List["PurchaseHistory"] = Relationship(back_populates="user")
    wishlist: List["Wishlist"] = Relationship(back_populates="user")
    reviews: List["Review"] = Relationship(back_populates="user")

class BookGenreLink(SQLModel, table=True):
    book_id: Optional[int] = Field(default=None, foreign_key="bookdetail.id", primary_key=True)
    genre_id: Optional[int] = Field(default=None, foreign_key="genre.id", primary_key=True)

class Genre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: Optional[str] = None
    books: List["BookDetail"] = Relationship(back_populates="genres", link_model=BookGenreLink)
    
class BookDetail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    author: str
    type: BookType = Field(nullable=False)
    isbn: Optional[str] = Field(unique=True)
    publisher: Optional[str] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    published_date: Optional[date] = None
    genres: List[Genre] = Relationship(back_populates="books", link_model=BookGenreLink)
    purchase_history: List["PurchaseHistory"] = Relationship(back_populates="book")
    tags: List["Tag"] = Relationship(back_populates="book")
    reviews: List["Review"] = Relationship(back_populates="book")
    wishlist: List["Wishlist"] = Relationship(back_populates="book")

class PurchaseHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="bookdetail.id")
    purchase_date: date = Field(nullable=False)
    price: Optional[float] = None
    location: Optional[str] = None
    quantity: int = Field(default=1)

    user: "User" = Relationship(back_populates="purchase_history")
    book: "BookDetail" = Relationship(back_populates="purchase_history")

class Wishlist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="bookdetail.id")
    added_date: date = Field(nullable=False)

    user: "User" = Relationship(back_populates="wishlist")
    book: "BookDetail" = Relationship(back_populates="wishlist")

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    book_id: int = Field(foreign_key="bookdetail.id")

    book: "BookDetail" = Relationship(back_populates="tags")

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    book_id: int = Field(foreign_key="bookdetail.id")
    review_text: str = Field(nullable=False)
    rating: int = Field(nullable=False)
    review_date: date = Field(nullable=False)

    user: "User" = Relationship(back_populates="reviews")
    book: "BookDetail" = Relationship(back_populates="reviews")

