# backend/app/ai.py
import os
import io
from typing import Optional

# --- Optional providers ---
USE_WEB = bool(os.getenv("GOOGLE_API_KEY"))
USE_VERTEX = bool(os.getenv("GOOGLE_CLOUD_PROJECT"))

# Web API (google-generativeai)
genai = None
if USE_WEB:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Vertex AI
vertexai = None
if USE_VERTEX:
    import vertexai
    from vertexai.generative_models import GenerativeModel, Part
    vertexai.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_REGION", "us-central1"),
    )

# ------------- Provider Abstraction -------------

def _text_model_name() -> str:
    # same name on both providers
    return os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

def _get_text_response(parts: list) -> str:
    """
    parts: list of strings and/or image bytes (we'll normalize per provider)
    Returns plain text, with safe fallback.
    """
    try:
        if USE_VERTEX:
            # Build Vertex inputs
            vparts = []
            for p in parts:
                if isinstance(p, bytes):
                    vparts.append(Part.from_data(mime_type="image/jpeg", data=p))
                else:
                    vparts.append(str(p))
            model = GenerativeModel(_text_model_name())
            resp = model.generate_content(vparts)
            return (resp.text or "").strip()
        elif USE_WEB:
            # Build Web API inputs
            wparts = []
            for p in parts:
                if isinstance(p, bytes):
                    wparts.append({"mime_type": "image/jpeg", "data": p})
                else:
                    wparts.append(str(p))
            model = genai.GenerativeModel(_text_model_name())
            resp = model.generate_content(wparts)
            return (resp.text or "").strip()
        else:
            # No provider configured
            return ""
    except Exception as e:
        # Never crash the app on AI failure
        return ""

# ------------- Public Helpers -------------

def generate_description(title: str, details: Optional[str] = None) -> str:
    prompt = f"""Write a short, engaging e-commerce description for a handmade artwork titled "{title}".
Keep it under 80 words, friendly, and descriptive. {('Details: '+details) if details else ''}"""
    text = _get_text_response([prompt])
    return text or f"{title}: a handcrafted original piece with care and detail."

def recommend_price(title: str, description: str = "") -> float:
    prompt = f"""Suggest a fair INR price (number only) for the handmade artwork below.
Title: {title}
Description: {description}
Only return a number."""
    text = _get_text_response([prompt])
    # Extract first number
    import re
    m = re.search(r"\d+(?:\.\d+)?", text or "")
    return float(m.group(0)) if m else 999.0

def suggest_hashtags(description: str) -> list[str]:
    prompt = f"""Suggest up to 5 concise hashtags (no # symbols, comma-separated)
for this handmade artwork description: {description}"""
    text = _get_text_response([prompt])
    tags = [t.strip().lstrip("#") for t in (text or "").split(",") if t.strip()]
    return tags[:5] if tags else ["handmade","art","local","craft","unique"]

def summarize_artwork(description: str) -> str:
    prompt = f"Summarize this artwork in one friendly sentence: {description}"
    return _get_text_response([prompt]) or description[:120]

def suggest_trending_designs() -> list[str]:
    prompt = "List 5 trending handmade design ideas, comma-separated."
    text = _get_text_response([prompt])
    ideas = [x.strip() for x in (text or "").split(",") if x.strip()]
    return ideas[:5] or [
        "Block-printed scarves", "Minimal line art", "Terracotta vases",
        "Upcycled jewelry", "Mysore-style floral motifs"
    ]

# --- Image quality & enhancement ---

from PIL import Image, ImageFilter, ImageOps

def check_image_quality(image_bytes: bytes) -> str:
    """
    Ask the model to approve/reject quality. Falls back to heuristic if AI unavailable.
    Returns 'APPROVE' or 'REJECT_QUALITY_ISSUE'
    """
    prompt = ("Analyze this product image quality (blur, lighting, composition). "
              "Return only APPROVE or REJECT_QUALITY_ISSUE.")
    text = _get_text_response([image_bytes, prompt])
    if text in ("APPROVE", "REJECT_QUALITY_ISSUE"):
        return text

    # Heuristic fallback if AI failed
    try:
        im = Image.open(io.BytesIO(image_bytes)).convert("L")
        var = ImageStat.Stat(im).var  # lazy variance check
    except Exception:
        var = 150.0
    return "APPROVE" if var > 100 else "REJECT_QUALITY_ISSUE"

def enhance_image(image_bytes: bytes) -> bytes:
    """Basic enhancement: auto-contrast + sharpen."""
    im = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    im = ImageOps.autocontrast(im)
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    out = io.BytesIO()
    im.save(out, format="JPEG", quality=92)
    return out.getvalue()

# --- Optional: simple text chat for chatbot ---

def chat_reply(question: str, catalog_text: str) -> str:
    prompt = f"""You are a friendly shopping assistant for a handmade local art marketplace.
User question: {question}
Catalog:
{catalog_text}
Recommend suitable items briefly."""
    return _get_text_response([prompt]) or "You can explore our latest pieces in the catalog!"
