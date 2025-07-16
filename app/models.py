from sqlalchemy import Column, String, ForeignKey, DateTime, Enum, Float, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum('client', 'fundi', 'admin', name='user_role'), nullable=False)
    location = Column(String)
    profile_picture = Column(String)

    fundi_profile = relationship("FundiProfile", back_populates="user", uselist=False)
    homeowner_profile = relationship("HomeOwnerProfile", back_populates="user", uselist=False)
    jobs = relationship("JobPosting", back_populates="client")
    sent_messages = relationship("Message", foreign_keys='Message.sender_id', back_populates="sender")
    received_messages = relationship("Message", foreign_keys='Message.receiver_id', back_populates="receiver")
    ratings_given = relationship("Rating", back_populates="rater")

# ───────────────────────────────────────────────

class FundiProfile(Base):
    __tablename__ = "fundis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    daily_rate = Column(Float)
    availability = Column(String)
    portfolio_items = Column(ARRAY(String))
    conditions = Column(Text)
    average_rating = Column(Float)

    user = relationship("User", back_populates="fundi_profile")
    ratings = relationship("Rating", back_populates="fundi")

# ───────────────────────────────────────────────

class HomeOwnerProfile(Base):
    __tablename__ = "homeowners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    bio = Column(Text)
    address = Column(String(100))
    preferred_payment_method = Column(String(50))

    user = relationship("User", back_populates="homeowner_profile")

# ───────────────────────────────────────────────

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    job_description = Column(String(300), nullable=False)
    location = Column(String(50))
    budget = Column(Float)
    timeline = Column(String(50))
    status = Column(Enum("open", "accepted", "completed", name='job_status'), default="open")

    client = relationship("User", back_populates="jobs")

# ───────────────────────────────────────────────

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    message = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

# ───────────────────────────────────────────────

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_postings.id"))
    rated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    fundi_id = Column(UUID(as_uuid=True), ForeignKey("fundis.id"))
    rating = Column(Float)
    review = Column(String(300))

    rater = relationship("User", back_populates="ratings_given")
    fundi = relationship("FundiProfile", back_populates="ratings")
