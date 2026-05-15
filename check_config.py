"""Quick config check"""
from dotenv import load_dotenv
import os

load_dotenv()

print("Current Configuration:")
print(f"API Key: {os.getenv('OPENROUTER_API_KEY')[:20]}...")
print(f"Base URL: {os.getenv('OPENAI_BASE_URL')}")
print(f"Model: {os.getenv('OPENAI_MODEL')}")
print(f"DEBUG: {os.getenv('DEBUG')}")
