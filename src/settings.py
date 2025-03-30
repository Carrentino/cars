from functools import lru_cache
from typing import Any

from fastapi_storages import S3Storage
from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(default='localhost:9092')
    group_id: str = Field(default='cars-group')
    topic_car_score: str = Field('cars_score')

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


class AWSSettings(BaseSettings):
    access_key: str = Field(default='admin')
    secret_access_key: str = Field(default='admin123')
    bucket: str = Field(default='cars')
    endpoint: str = Field(default='localhost:9000')
    default_acl: str = Field(default='public-read')
    use_ssl: bool = Field(default=False)
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix='aws_',
    )


class AssetS3Storage(S3Storage):  # type: ignore
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
    AWS_S3_BUCKET_NAME = None
    AWS_S3_ENDPOINT_URL = None
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_USE_SSL = True

    def __init__(self, *_args: Any, **kwargs: Any) -> None:
        self.AWS_ACCESS_KEY_ID = kwargs.get('aws_access_key')
        self.AWS_SECRET_ACCESS_KEY = kwargs.get('aws_secret_access_key')
        self.AWS_S3_BUCKET_NAME = kwargs.get('aws_bucket')
        self.AWS_S3_ENDPOINT_URL = kwargs.get('aws_endpoint')
        self.AWS_DEFAULT_ACL = kwargs.get('aws_default_acl', 'public-read')
        self.AWS_S3_USE_SSL = kwargs.get('aws_use_ssl', True)
        super().__init__()


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
    aws: AWSSettings = AWSSettings()
    crypto_key: bytes = Field(
        default=b'\x17]~X#\r\xbb\xf3X\x88\x92}\x9aj\xa4\xcd\xe3\xdfZ\xe7\xdaF\xca\xbe\xfb\x9d\x9c\x08\x9eY2\xa6'
    )

    @property
    def storage(self):
        return AssetS3Storage(
            aws_access_key=self.aws.access_key,
            aws_secret_access_key=self.aws.secret_access_key,
            aws_bucket=self.aws.bucket,
            aws_endpoint=self.aws.endpoint,
            aws_default_acl=self.aws.default_acl,
            aws_use_ssl=self.aws.use_ssl,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
