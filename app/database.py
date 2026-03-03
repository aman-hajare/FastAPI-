from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' #'postgresql://<username>:<password>@<ip-address/hostname:port>/<database_name>'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()














## if we want raw sql (less functionallity but fast and raw sql allow)
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:    
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")    
#         print("Error: ", error)
#         time.sleep(2)