from pydantic import BaseModel
from typing import Optional

# ------------------ USERS ------------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
    
    # --- NEW/UPDATED FIELDS FOR REGISTRATION ---
    phone_number: Optional[str] = None           # 👈 NEW
    preferred_language: Optional[str] = "en"     # 👈 NEW
    latitude: Optional[float] = None             # 👈 NEW
    longitude: Optional[float] = None            # 👈 NEW
    address: Optional[str] = None                # 👈 NEW
    proof_url: Optional[str] = None              # 👈 UPDATED (for the uploaded document link)
    # -------------------------------------------


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_verified: bool
    verification_status: str
    
    # --- NEW FIELDS FOR RESPONSE ---
    phone_number: Optional[str] = None           # 👈 NEW
    preferred_language: str                      # 👈 NEW
    address: Optional[str] = None                # 👈 NEW
    # -------------------------------

    class Config:
        orm_mode = True
# ... (rest of file remains the same)