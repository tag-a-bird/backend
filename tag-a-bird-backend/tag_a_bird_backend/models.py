from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import  sessionmaker, scoped_session, declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

    annotations = relationship("Annotation", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, password={self.password!r})"

class Annotation(Base):
    __tablename__ = "annotation"

    id = Column(Integer, primary_key=True)
    recording_id = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="annotations")
    start_time = Column(Integer)
    end_time = Column(Integer)
    label = Column(String)

    def __repr__(self):
        return f"Annotation(id={self.id!r}, recording_id={self.recording_id!r}, user_id={self.user_id!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, label={self.label!r})"
