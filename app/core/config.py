from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Parenting App"
    debug: bool = False
    database_url: str = ""
    openai_api_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
