from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# For connecting to a SQLite database & opening a file with the SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# similar connection to postgresql database
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Creating a sql database engine. "check_same_thread": False is only required for sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Creating a SessionLocal. Each instance of the SessionLocal class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating a Base class.
# Later we will inherit from this class to create each of the database models or classes
Base = declarative_base()
