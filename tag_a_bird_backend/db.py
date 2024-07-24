from sqlalchemy import create_engine, func, pool
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

Base = declarative_base()
engine = None
Session = sessionmaker()
db_session = scoped_session(Session)

def configure_engine(url):
    global engine, db_session, Session

    engine = create_engine(url, poolclass=pool.NullPool)
    db_session.remove()
    Session.configure(bind=engine)
    db_session.configure(bind=engine)
    Base.metadata.create_all(engine)

def get_engine():
    global engine
    return engine