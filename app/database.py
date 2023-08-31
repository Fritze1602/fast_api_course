from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

from sqlalchemy.util import deprecations
deprecations.SILENCE_UBER_WARNING = True

SQLALCHEMY_DATABASE_URL = f"postgresql://{get_settings().database_username}:{get_settings().database_password}@{get_settings().database_hostname}:{get_settings().database_port}/{get_settings().database_name}"

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:Zauberer@localhost:5432/fastapi_course"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Nur für Raw SQL mit psycopg2!!!
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi_course", user="postgres", password="Zauberer", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connection was successfull")
#         break
#     except Exception as error:
#         print("Connecting to db failed")
#         print("Error: ", error)
#         time.sleep(2)
