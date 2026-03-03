import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-keep-it-safe")

RATE_LIMIT = "5/minute"

VALID_SECTORS = [
    "pharmaceuticals", "technology", "agriculture",
    "automobile", "textiles", "chemicals",
    "electronics", "energy", "finance", "retail"
]