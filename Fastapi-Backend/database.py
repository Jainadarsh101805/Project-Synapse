# database.py

from sqlmodel import create_engine, Session, SQLModel

# 1. Define the database URL
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# 2. Create the database engine
# connect_args={"check_same_thread": False} is required for SQLite when using it with FastAPI
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

# 3. Function to create tables (called once at startup)
def create_db_and_tables():
    """Initializes the database and creates all defined SQLModel tables."""
    SQLModel.metadata.create_all(engine)

# 4. Dependency function to yield a database session
def get_session():
    """Dependency function to manage a database session per request."""
    with Session(engine) as session:
        yield session