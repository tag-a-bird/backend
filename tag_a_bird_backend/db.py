import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

engine = create_engine(os.getenv('FLASK_DATABASE_URI'))

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)
    )

Base.query = db_session.query_property()

Base.metadata.create_all(engine)