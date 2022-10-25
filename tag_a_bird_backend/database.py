from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = None
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)
    )

Base = declarative_base()

Base.query = db_session.query_property()

def init_engine(uri, **kwargs):
  global engine
  engine = create_engine(uri, **kwargs)
  return engine

def init_db():
    import tag_a_bird_backend.models
    Base.metadata.create_all(engine)
    