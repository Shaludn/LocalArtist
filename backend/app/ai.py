import os
import io
import google.generativeai as genai
from google.cloud import speech

# -----------------------------
# Gemini Configuration
# -----------------------------
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("⚠️ GOOGLE_API_KEY not set in environment variables")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# Google Speech-to-Text
# -----------------------------
speech_client = speech.SpeechClient()

def speech_to_text(audio_bytes: bytes, language_code: str = "hi-IN") -> str:
    """
    Convert audio (wav/mp3 bytes) to text using Google Cloud Speech-to-Text.
    Default language = Hindi ("hi-IN"). Change language_code for others.
    """
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
    )
    response = speech_client.recognize(config=config, audio=audio)

    if not response.results:
        return ""
    return response.results[0].alternatives[0].transcript

# -----------------------------
# 1. Translation
# -----------------------------
def translate_text(text: str, target_lang: str = "en") -> str:
    prompt = f"Translate the following text into {target_lang}:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# -----------------------------
# 2. Generate Artwork Description
# -----------------------------
def generate_description(title: str, original_desc: str = None) -> str:
    prompt = f"Write a beautiful, marketing-friendly description for this handmade item: {title}."
    if original_desc:
        prompt += f"\nSeller provided details: {original_desc}"
    response = model.generate_content(prompt)
    return response.text.strip()

# -----------------------------
# 3. Recommend Price
# -----------------------------
def recommend_price(title: str, description: str = "") -> float:
    prompt = (
        f"Suggest a reasonable price (in USD) for a handmade product titled '{title}' "
        f"with details: {description}. Return only a number."
    )
    response = model.generate_content(prompt)
    try:
        return float(response.text.strip().split()[0])
    except:
        return 100.0  # fallback

# -----------------------------
# 4. Summarize Artwork
# -----------------------------
def summarize_artwork(description: str) -> str:
    prompt = f"Summarize this artwork description in one short, catchy sentence:\n\n{description}"
    response = model.generate_content(prompt)
    return response.text.strip()

# -----------------------------
# 5. Suggest Hashtags
# -----------------------------
def suggest_hashtags(description: str) -> list[str]:
    prompt = (
        f"Generate 5 short hashtags for promoting this handmade product on social media.\n"
        f"Description: {description}"
    )
    response = model.generate_content(prompt)
    hashtags = [tag.strip() for tag in response.text.split() if tag.startswith("#")]
    return hashtags or ["#Handmade", "#Artisan", "#Unique", "#Crafts", "#SupportLocal"]

# -----------------------------
# 6. Voice-to-Artwork Pipeline
# -----------------------------
def process_voice_artwork(audio_bytes: bytes, lang: str = "hi-IN") -> dict:
    """
    Full pipeline:
    1. Voice → Text (native language)
    2. Translate to English
    3. Generate English marketing description
    """
    native_text = speech_to_text(audio_bytes, language_code=lang)
    translated = translate_text(native_text, "en")
    description = generate_description("Handmade Artwork", translated)
    return {
        "native_text": native_text,
        "translated_text": translated,
        "ai_description": description,
    }
