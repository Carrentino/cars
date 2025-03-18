from functools import lru_cache

from fastapi_storages import FileSystemStorage
from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    bootstrap_servers: str
    group_id: str
    topic_car_score: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix='kafka_',
    )

    @property
    def topics(self) -> list[str]:
        return [v for k, v in self.__dict__.items() if k.startswith('topic_')]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
    )

    host: str = '127.0.0.1'
    port: int = 8080
    workers_count: int = 1
    reload: bool = True

    log_level: str = Field(default='info')
    debug: bool = True
    debug_postgres: bool = False

    environment: str = 'dev'

    postgres_dsn: PostgresDsn = Field(  # type: ignore
        default='postgresql+asyncpg://postgres:postgres@localhost:5432/base'
    )
    test_postgres_dsn: PostgresDsn = Field(  # type: ignore
        default='postgresql+asyncpg://postgres:@localhost:5432/carrentino_cars_test'
    )

    trace_id_header: str = 'X-Trace-Id'
    jwt_key: SecretStr = Field(default=SecretStr('551b8ef09b5e43ddcc45461f854a89b83b9277c6e578f750bf5a6bc3f06d8c08'))
    reviews_url: str = Field(default='https://carrentino.ru/reviews/api/cars')
    kafka: KafkaSettings = KafkaSettings()

    @property
    def storage(self):
        return FileSystemStorage(path="uploads/")


@lru_cache
def get_settings() -> Settings:
    return Settings()
