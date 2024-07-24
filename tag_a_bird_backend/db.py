import time
from sqlalchemy import create_engine, func, pool
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError

Base = declarative_base()
engine = None
Session = sessionmaker()
db_session = scoped_session(Session)

def configure_engine(url, retries=5, delay=5):
    global engine, db_session, Session

    while retries > 0:
        try:
            engine = create_engine(url, poolclass=pool.NullPool)
            db_session.remove()
            Session.configure(bind=engine)
            db_session.configure(bind=engine)
            Base.metadata.bind = engine  # Bind the metadata to the engine
            Base.metadata.create_all(engine)
            return
        except OperationalError:
            retries -= 1
            if retries > 0:
                print(f"Database connection failed. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise Exception("Database connection failed after retries")

def get_engine():
    global engine
    return engine