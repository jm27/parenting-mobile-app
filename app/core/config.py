from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App Settings
    app_name: str = "Parenting App"
    debug: bool = True

    # Database
    database_url: str = "sqlite:///./parenting_app.db"

    # OpenAI
    openai_api_key: str = ""

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Debug: Print if OpenAI key is loaded (first few characters only for security)
        if self.debug and self.openai_api_key:
            print(f"✅ OpenAI API Key loaded: {self.openai_api_key[:8]}...")
        elif self.debug:
            print("❌ OpenAI API Key not found!")


settings = Settings()
