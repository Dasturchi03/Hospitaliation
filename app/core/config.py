from typing import Optional
from pydantic import field_serializer, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    PROJECT_NAME: str = "Template-app"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DATABASE_URL: str = Field(default='')

    MINIO_BUCKETNAME: str = "app"
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_TAG: str = 'miniofile'

    HTTP_PROXY: Optional[str] = None
    HTTPS_PROXY: Optional[str] = None

    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra='allow')

    def model_post_init(self, __context):
        self.DATABASE_URL = URL.create(
            drivername='postgresql+psycopg2',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB
        )

settings = Settings()
