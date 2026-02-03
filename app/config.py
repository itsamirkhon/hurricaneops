"""
Configuration management for the Emergency Coordination System.
Loads settings from environment variables.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment."""
    
    # Cerebras API Configuration
    CEREBRAS_API_KEY: str = os.getenv("CEREBRAS_API_KEY", "")
    CEREBRAS_MODEL: str = os.getenv("CEREBRAS_MODEL", "gpt-oss-120b")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Application Settings
    APP_NAME: str = "AI Emergency Coordination System"
    APP_VERSION: str = "1.0.0"
    
    @property
    def is_configured(self) -> bool:
        """Check if the application is properly configured."""
        return bool(self.CEREBRAS_API_KEY and self.CEREBRAS_API_KEY != "your_api_key_here")


settings = Settings()
