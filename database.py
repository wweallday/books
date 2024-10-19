import psycopg2
from psycopg2 import sql
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker

# Create a connection to the server (without specifying a database)
conn = psycopg2.connect(
    dbname='postgres', user='postgres', password='a', host='192.168.1.135', port='54322'
)
conn.autocommit = True
cursor = conn.cursor()

# Create the 'books' database if it doesn't exist
try:
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('books')))
except psycopg2.errors.DuplicateDatabase:
    print("Database already exists")
finally:
    cursor.close()
    conn.close()

# Connect to the new 'books' database and create the engine
DATABASE_URL = "postgresql://postgres:a@192.168.1.135:54322/books"
engine = create_engine(DATABASE_URL, echo=False)  # Set echo to False to reduce logs

# Create a SessionLocal class that will serve as a factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database (only creates tables if they don't exist)
def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
