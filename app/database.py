from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

session = None

Base = declarative_base()

def init_db(db_string):
    global session
    engine = create_engine(db_string)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False,bind=engine))
    import app.models
    Base.metadata.create_all(engine)