# backend/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

import backend.app.models as models
from backend.app.database import engine
from backend.routes import auth, artworks, requests, seller, admin, orders, notifications, seed, seller_ai, ai_routes, ar_routes, chatbot
from backend.dependencies import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Local Artisans Marketplace - Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)
# main.py — add BEFORE app.include_router(...)
from sqlalchemy import text
from backend.app.database import engine

def _colnames(conn, table):
    rows = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
    return {r[1] for r in rows}  # r[1] = column name

def run_light_migrations():
    with engine.begin() as conn:
        cols = _colnames(conn, "users")

        # add only what’s missing
        if "phone_number" not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone_number VARCHAR"))
        if "preferred_language" not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN preferred_language VARCHAR DEFAULT 'en'"))
        if "latitude" not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN latitude REAL"))
        if "longitude" not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN longitude REAL"))
        if "address" not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN address VARCHAR"))
        if "proof_url" not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN proof_url VARCHAR"))
        if "verification_status" not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN verification_status VARCHAR DEFAULT 'pending'"))
        if "is_verified" not in cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT 0"))

# call it right after creating tables:
models.Base.metadata.create_all(bind=engine)
run_light_migrations()


# Routers
app.include_router(auth.router)
app.include_router(artworks.router)
app.include_router(requests.router)
app.include_router(seller.router)
app.include_router(admin.router)
app.include_router(orders.router)
app.include_router(notifications.router)
app.include_router(seed.router)
app.include_router(seller_ai.router)
app.include_router(ai_routes.router)
app.include_router(ar_routes.router)
app.include_router(chatbot.router)

# Static assets for uploads
Path("static").mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Only mount frontend if it exists
if Path("frontend").exists():
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
def root():
    return {"message": "Local Artisans Marketplace backend running"}

# backend/main.py (add near the bottom)
from pathlib import Path
from fastapi.staticfiles import StaticFiles

static_dir = Path("static")
static_dir.mkdir(parents=True, exist_ok=True)  # for proofs/artworks

frontend_dir = Path("frontend")
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

