from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy.types import Boolean, DateTime, Integer, String
from .db import Base

class User(Base, UserMixin):
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

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(
            password,
            method='sha256'
        )

    def verify_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)

    annotations = relationship("Annotation", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, password={self.password!r})"

class QueryConfig(Base):
    __tablename__ = "query_config"

    parameter = Column(
        String(100),
        primary_key=True,
        unique=True,
        nullable=False
    )
    value = Column(
        String(100),
        nullable=True,)


    def __repr__(self):
        return f"QueryConfig(parameter={self.parameter!r}, value={self.value!r})"

class Annotation(Base):
        __tablename__ = "annotation"

        id = Column(Integer, primary_key=True, autoincrement=True)
        recording_id = Column(Integer, ForeignKey("record.id"))
        record = relationship("Record", back_populates="annotations")
        user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
        user = relationship("User", back_populates="annotations")
        start_time = Column(Integer , nullable=False)
        end_time = Column(Integer, nullable=False)
        label = Column(String)
        status = Column(String)
        comment = Column(String)
        created_at = Column(
            DateTime,
            default=datetime.utcnow()
        )

        def __repr__(self):
            return f"Annotation(id={self.id!r}, recording_id={self.recording_id!r}, user_id={self.user_id!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, label={self.label!r}, self.status={self.status!r})"

class Record(Base):
        __tablename__ = "record"

        id = Column(Integer, primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow())
        audio_url = Column(String)
        photo_url = Column(String)
        comment = Column(String)
        country = Column(String)
        city = Column(String)
        habitat = Column(String)
        species = Column(String)
        weather = Column(String)
        date = Column(DateTime)
        device_os = Column(String)
        is_holiday = Column(Boolean)
        human_noise = Column(Boolean)
        device_model = Column(String)
        habitat_other = Column(String)
        species_other = Column(String)
        day_of_the_week = Column(String)
        human_noise_type = Column(String)
        location_private = Column(Boolean)
        location_accuracy = Column(String)
        dawn_chorus_import_id = Column(String)
        human_noise_intensity = Column(String)
        organization_membership = Column(String)
        advanced_audio_equipment = Column(String)
        status = Column(String)

        annotations = relationship("Annotation", back_populates="record")

        def __repr__(self):
            return f"Record(id={self.id!r}, audio_url={self.audio_url!r}, photo_url={self.photo_url!r}, comment={self.comment!r}, country={self.country!r}, city={self.city!r}, habitat={self.habitat!r}, species={self.species!r}, weather={self.weather!r}, date={self.date!r}, device_os={self.device_os!r}, is_holiday={self.is_holiday!r}, human_noise={self.human_noise!r}, device.model={self.device.model!r}, habitat_other={self.habitat_other!r}, species_other={self.species_other!r}, day_of_the_week={self.day_of_the_week!r}, human_noise_type={self.human_noise_type!r}, location_private={self.location_private!r}, location_accuracy={self.location_accuracy!r}, dawn_chorus_import_id={self.dawn_chorus_import_id!r}, human_noise_intensity={self.human_noise_intensity!r}, organization_membership={self.organization_membership!r}, advanced_audio_equipment={self.advanced_audio_equipment!r}, status={self.status!r})"

        #method to deserialize given json to Record object
        @staticmethod
        def from_json(json, id):
            record = Record()
            record.id = id
            record.audio_url = json.get('audio')
            record.photo_url = json.get('photo')
            record.comment = json.get('comment')
            record.country = json.get('country')
            record.city = json.get('city')
            record.habitat = json.get('habitat')
            record.species = json.get('species')
            record.weather = json.get('weather')
            record.date = datetime.fromisoformat(json.get('date_time')[:-1] + '+00:00').astimezone(timezone.utc)
            record.device_os = json.get('device_os')
            record.is_holiday = bool(json.get('is_holiday'))
            record.human_noise = bool(json.get('human_noise'))
            record.device_model = json.get('device_model')
            record.habitat_other = json.get('habitat_other')
            record.species_other = json.get('species_other')
            record.day_of_the_week = json.get('day_of_the_week')
            record.human_noise_type = json.get('human_noise_type')
            record.location_private = bool(json.get('location_private'))
            record.location_accuracy = json.get('location_accuracy')
            record.dawn_chorus_import_id = json.get('dawn_chorus_import_id')
            record.human_noise_intensity = json.get('human_noise_intensity')
            record.organization_membership = json.get('organization_membership')
            record.advanced_audio_equipment = json.get('advanced_audio_equipment')
            return record
