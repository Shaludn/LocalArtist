# backend/routes/seed.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
import backend.app.models as models
import backend.app.auth_utils as auth_utils

router = APIRouter(prefix="/seed", tags=["seed"])

@router.post("/")
def seed_data(db: Session = Depends(get_db)):
    # Clear existing data (optional for demo resets)
    db.query(models.Order).delete()
    db.query(models.Notification).delete()
    db.query(models.ArtRequest).delete()
    db.query(models.Artwork).delete()
    db.query(models.User).delete()
    db.commit()

    # Create Admin
    admin = models.User(
        username="admin",
        email="admin@example.com",
        password=auth_utils.hash_password("admin123"),
        role="admin",
        is_verified=True,
        verification_status="verified",
        preferred_language="en"
    )

    # Create Seller (with Location and Proof for verification)
    seller = models.User(
        username="seller",
        email="seller@example.com",
        password=auth_utils.hash_password("seller123"),
        role="seller",
        is_verified=True,
        verification_status="verified",
        phone_number="9876543210",
        preferred_language="hi",
        latitude=12.9716,     # Example: Bengaluru Lat
        longitude=77.5946,    # Example: Bengaluru Lon
        address="10, Artisan Street, Bengaluru, India",
        proof_url="http://example.com/seller_pan.pdf"
    )

    # Create Customer (with Location)
    customer = models.User(
        username="customer",
        email="customer@example.com",
        password=auth_utils.hash_password("customer123"),
        role="customer",
        is_verified=True,
        verification_status="verified",
        preferred_language="kn",
        latitude=13.0827,     # Example: Slightly different location
        longitude=80.2707,    # Example: Chennai Lon (far from seller)
        address="22, Customer Lane, Chennai, India"
    )

    db.add_all([admin, seller, customer])
    db.commit()
    db.refresh(admin)
    db.refresh(seller)
    db.refresh(customer)

    # Add Artwork for seller
    artwork = models.Artwork(
        title="Handmade Vase",
        description="A beautiful handmade clay vase",
        price=150.0,
        image_url="http://example.com/vase.jpg",
        owner_id=seller.id
    )
    
    # Add a second artwork
    artwork2 = models.Artwork(
        title="Intricate Block-Printed Scarf",
        description="Soft organic cotton scarf with traditional block printing.",
        price=75.0,
        image_url="http://example.com/scarf.jpg",
        owner_id=seller.id
    )
    
    db.add_all([artwork, artwork2])
    db.commit()
    db.refresh(artwork)
    db.refresh(artwork2)

    return {
        "message": "Seed data created!",
        "admin": {"email": admin.email, "password": "admin123"},
        "seller": {"email": seller.email, "password": "seller123", "location": "Bengaluru"},
        "customer": {"email": customer.email, "password": "customer123", "location": "Chennai"},
        "artwork": {"id": artwork.id, "title": artwork.title}
    }