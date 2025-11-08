# backend/app/models.py

from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base

# ---------------- USER ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, index=True, nullable=False)

    # Email optional now
    email = Column(String, unique=True, index=True, nullable=True)

    # Phone is required & unique
    phone_number = Column(String, unique=True, index=True, nullable=False)

    password = Column(String, nullable=False)
    role = Column(String, default="seller")
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String, default="pending")

    # Verification fields
    proof_url = Column(String, nullable=True)
    preferred_language = Column(String, default="en")

    # GPS location (auto-detect at registration)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)

    # Relationship to artworks
    artworks = relationship("Artwork", back_populates="owner")


# ---------------- ARTWORK ----------------
class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False, default=0.0)
    image_url = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="artworks")


# ---------------- ORDER ----------------
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    artwork_id = Column(Integer, ForeignKey("artworks.id"))
    quantity = Column(Integer, default=1)
    status = Column(String, default="pending")


# ---------------- REQUEST ----------------
class ArtRequest(Base):
    __tablename__ = "art_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    requester_id = Column(Integer, ForeignKey("users.id"))


# ---------------- NOTIFICATION ----------------
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
