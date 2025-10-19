import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(backend_root))

print("=== API Key Debug ===")

# Check if .env file exists
env_file = backend_root / ".env"
print(f".env file exists: {env_file.exists()}")
print(f".env file path: {env_file}")

if env_file.exists():
    with open(env_file) as f:
        content = f.read()
        lines = content.split("\n")
        for line in lines:
            if "OPENAI_API_KEY" in line:
                print(f"Raw line from .env: '{line}'")
                # Check for common issues
                if line.endswith(" "):
                    print("⚠️  Line ends with space!")
                if "\r" in line:
                    print("⚠️  Line contains carriage return!")

# Load through settings
from app.core.config import settings

print(f"\nLoaded key: '{settings.openai_api_key}'")
print(f"Key length: {len(settings.openai_api_key)}")
print(f"Key starts with 'sk-': {settings.openai_api_key.startswith('sk-')}")
print(f"Key has spaces: {' ' in settings.openai_api_key}")
print(f"Key first 15 chars: '{settings.openai_api_key[:15]}'")
print(f"Key last 10 chars: '{settings.openai_api_key[-10:]}'")

# Check environment variable directly
direct_key = os.getenv("OPENAI_API_KEY")
print(f"\nDirect os.getenv: '{direct_key}'")
print(f"Keys match: {settings.openai_api_key == direct_key}")
