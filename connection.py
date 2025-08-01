from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

username = "root"
password = "2480"
database = "student_info_db"

Database_url = f"mysql+pymysql://{username}:{password}@localhost/{database}"

engine = create_engine(Database_url, echo=True)

SessionLocal = sessionmaker(bind=engine)


session = SessionLocal()

Base = declarative_base()