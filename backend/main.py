from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import backend.app.models as models
from backend.app.database import engine
from backend.routes import auth, artworks, requests, seller, admin
from backend.dependencies import get_current_user

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Local Artisans Marketplace - Prototype")

# Enable CORS (optional for frontend use later)
app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(artworks.router)
app.include_router(requests.router)
app.include_router(seller.router)
app.include_router(admin.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Local Artisans Marketplace Prototype running!"}

# Test: current authenticated user
@app.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Return info about the currently authenticated user.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "is_verified": current_user.is_verified,
        "verification_status": current_user.verification_status,
    }
from backend.routes import auth, artworks, requests, seller, admin, orders, notifications, seed, seller_ai, ai_routes

# Existing routers
app.include_router(auth.router)
app.include_router(artworks.router)
app.include_router(requests.router)
app.include_router(seller.router)
app.include_router(admin.router)
app.include_router(orders.router)
app.include_router(notifications.router)
app.include_router(seed.router)
app.include_router(seller_ai.router)
app.include_router(ai_routes.router)   # 👈 NEW
from backend.routes import ar_routes, chatbot

app.include_router(ar_routes.router)
app.include_router(chatbot.router)

from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
