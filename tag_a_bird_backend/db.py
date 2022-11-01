from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, create_session, sessionmaker

Base = declarative_base()
engine = None
sessionmaker = sessionmaker()
db_session = scoped_session(sessionmaker)

def configure_engine(url):
    global sessionmaker, engine, db_session

    engine = create_engine(url)
    db_session.remove()
    sessionmaker.configure(bind=engine)
    Base.metadata.create_all(engine)