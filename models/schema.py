from enum import Enum

class BookType(str, Enum):
    MANGA = "Manga"
    LIGHT_NOVEL = "Light Novel"
    SPECIAL = "Special"
    OTHER = "Other"