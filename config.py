import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration from environment variables."""
    
    # OpenRouter API settings
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "meta-llama/llama-3-8b-instruct")
    
    # Application settings
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY not found in environment. "
                "Please create a .env file with your API key."
            )
        return True

# Validate configuration on import
Config.validate()
