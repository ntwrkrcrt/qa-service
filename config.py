from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    DATABASE_URL: str
    DB_POOL_SIZE: int
    DB_MAX_OVERFLOW: int
    DB_POOL_TIMEOUT: int
    DB_ECHO: bool

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # CORS Security
    allowed_origins: list[str] = [
        "http://localhost:8000",
        "http://localhost:8080",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
