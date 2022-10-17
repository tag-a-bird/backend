from concurrent.futures import process
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True
    )
    username = Column(
        String(100),
        nullable=False,
        unique=False
    )
    email = Column(
        String(40),
        unique=True,
        nullable=False
    )
    password_hash = Column(
        String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    created_on = Column(
        DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    # last_login = Column(
    #     DateTime,
    #     index=False,
    #     unique=False,
    #     nullable=True
    # )

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(
            password,
            method='sha256'
        )

    def verify_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)

    def obj_to_dict(self):  # to build json format
        return {
            "id": self.id,
            "username": self.username,
            "email" : self.email,
            "password_hash" : self.password_hash,
            "created_on": self.created_on
        }

    annotations = relationship("Annotation", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, password={self.password!r})"

class Annotation(Base):
    __tablename__ = "annotation"

    id = Column(Integer, primary_key=True)
    recording_id = Column(Integer)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", back_populates="annotations")
    start_time = Column(Integer)
    end_time = Column(Integer)
    label = Column(String)

    def __repr__(self):
        return f"Annotation(id={self.id!r}, recording_id={self.recording_id!r}, user_id={self.user_id!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, label={self.label!r})"


class TokenBlocklist(Base):
    __tablename__ = "blocklist"

    id = Column(Integer, primary_key=True)
    jti = Column(UUID, nullable=False, index=True)
    created_at = Column(String(32), nullable=False)

def __repr__(self):
    return f"Annotation(id={self.id!r}, jti={self.jti!r})"
