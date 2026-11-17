from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    secret_key: str
    environment: str
    database_url : str
    jwt_algorithm : str
    jwt_access_token_expire_minutes : int
    jwt_refresh_token_expire_days : int

settings = Settings()