
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="seller")  # seller or customer
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String, default="pending")  # pending/verified/rejected
    
    # --- EXISTING FIELD, RENAMED/CLARIFIED ---
    proof_url = Column(String, nullable=True) # e.g., GST/PAN document URL
    
    # --- NEW FIELDS FOR REGISTRATION/VERIFICATION ---
    phone_number = Column(String, nullable=True)     # 👈 NEW
    preferred_language = Column(String, default="en") # 👈 NEW (e.g., 'en', 'hi', 'kn')
    latitude = Column(Float, nullable=True)          # 👈 NEW (for location)
    longitude = Column(Float, nullable=True)         # 👈 NEW (for location)
    address = Column(String, nullable=True)          # 👈 NEW (for artisan address)
    # -----------------------------------------------

    artworks = relationship("Artwork", back_populates="owner")
# ... (rest of file remains the same)
