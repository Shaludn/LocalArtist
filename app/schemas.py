# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional

# ------------------ USERS ------------------
class UserCreate(BaseModel):
    username: str
    phone_number: str
    password: str
    role: str  # "seller" | "customer"

    # Registration extras
    preferred_language: Optional[str] = "en"
    # GPS comes from device at registration time (frontend fills these)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None  # optional text label (reverse-geocode / map pick)
    proof_url: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    is_verified: bool
    verification_status: str

    phone_number: Optional[str] = None
    preferred_language: str
    address: Optional[str] = None

    class Config:
        orm_mode = True

# ------------------ ARTWORKS ------------------
class ArtworkBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = 0.0
    image_url: Optional[str] = None

class ArtworkCreate(ArtworkBase):
    pass

class ArtworkResponse(ArtworkBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

# ------------------ ORDERS ------------------
class OrderResponse(BaseModel):
    id: int
    customer_id: int
    artwork_id: int
    quantity: int
    status: str
    class Config:
        orm_mode = True

# ------------------ NOTIFICATIONS ------------------
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    class Config:
        orm_mode = True

# ------------------ REQUESTS ------------------
class RequestResponse(BaseModel):
    id: int
    title: str
    description: str
    requester_id: int
    class Config:
        orm_mode = True

# ------------------ LOGIN ------------------
class UserLogin(BaseModel):
    phone_number: str
    password: str
