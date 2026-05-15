"""Quick test script to check for import errors"""
import sys
print("Python version:", sys.version)
print("\nTesting imports...")

try:
    print("✓ Importing config...")
    from config import Config
    print(f"  API Key exists: {bool(Config.OPENROUTER_API_KEY)}")
    
    print("✓ Importing database...")
    from database import init_db, Interview, Question
    
    print("✓ Importing utils...")
    from utils import extract_text_from_pdf
    
    print("✓ Importing pipeline...")
    from pipeline import run_pipeline, evaluate_answer
    
    print("✓ Importing FastAPI...")
    from fastapi import FastAPI
    
    print("✓ Importing main...")
    import main
    
    print("\n✅ All imports successful!")
    print("\nTo start the backend, run:")
    print("  python -m uvicorn main:app --reload")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
