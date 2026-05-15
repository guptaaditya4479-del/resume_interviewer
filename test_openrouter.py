"""Test script to verify OpenRouter API and find working models"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Updated list with correct OpenRouter model names (2024)
test_models = [
    # Free models
    "meta-llama/llama-3.2-3b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemini-flash-1.5",
    "google/gemini-pro-1.5",
    
    # Paid models (cheaper options)
    "meta-llama/llama-3-8b-instruct",
    "mistralai/mistral-7b-instruct-v0.3",
    "anthropic/claude-3-haiku",
    "openai/gpt-3.5-turbo",
    "google/gemini-flash-1.5-8b",
    
    # Alternative free options
    "nousresearch/hermes-3-llama-3.1-405b:free",
]

print("="*60)
print("Testing OpenRouter Models")
print("="*60)

working_models = []
failed_models = []

for model in test_models:
    try:
        print(f"\n🔍 Testing: {model}...")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'OK'"}],
            max_tokens=10,
            temperature=0
        )
        result = response.choices[0].message.content
        print(f"✅ SUCCESS!")
        print(f"   Response: {result}")
        working_models.append(model)
    except Exception as e:
        error_msg = str(e)
        print(f"❌ FAILED")
        print(f"   Error: {error_msg[:100]}")
        failed_models.append((model, error_msg))

print("\n" + "="*60)
print("SUMMARY")
print("="*60)

if working_models:
    print(f"\n✅ WORKING MODELS ({len(working_models)}):")
    for i, model in enumerate(working_models, 1):
        print(f"   {i}. {model}")
    print(f"\n🎯 RECOMMENDED: Use '{working_models[0]}' in your .env file")
    print(f"\n   Update OPENAI_MODEL={working_models[0]}")
else:
    print("\n❌ No working models found!")
    print("   Please check your OpenRouter API key")

print(f"\n❌ Failed models: {len(failed_models)}")
print("\nTest complete!")
