import hashlib
import hmac
import os
import logging
from pathlib import Path
from typing import Optional, Union

from dotenv import load_dotenv
from dataclasses import dataclass, field
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).parent.parent


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass(frozen=True)
class AuthJWTConfig:
    bot_token: str = os.environ.get("BOT_TOKEN", '123')
    secret_key: str = hmac.new(bot_token.encode('utf-8'), "WebAppData".encode('utf-8'), hashlib.sha256).hexdigest()
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 30

@dataclass
class YandexAPIConfig:
    TOKEN_FOR_GEOSUGGEST: Optional[str] = os.getenv("TOKEN_FOR_GEOSUGGEST")
    TOKEN_FOR_GEOCODER: Optional[str] = os.getenv("TOKEN_FOR_GEOCODER")



@dataclass
class MongoDBConfig:
    host: Optional[str] = 'localhost'
    port: Union[str, int] = 27017
    database: str = os.getenv("MONGO_DATABASE", 'db')
    menu_collection: str = os.getenv("MENU_COLLECTION", 'collection')
    test_menu_collection: str = os.getenv("TEST_MENU_COLLECTION", 'test')
    url: str = f"mongodb://{host}:{port}"

@dataclass
class S3Config:
    access_key: Optional[str] = os.getenv("S3_ACCESS_KEY")
    secret_key: Optional[str] = os.getenv("S3_SECRET_KEY")
    bucket_name: Optional[str] = os.getenv("S3_BACKET_NAME")

@dataclass
class DatabaseConfig:
    """Database connection variables."""

    name: Optional[str] = os.getenv('DBNAME')
    test_name: Optional[str] = os.getenv("TEST_DB_NAME")
    user: Optional[str] = 'postgres' #"backend"
    password: Optional[str] = 'Tosya1253' #os.getenv('BACKEND_PASSWORD', None)
    port: int = 5432
    host: str = 'localhost' #'db'

    driver: str = 'asyncpg'
    database_system: str = 'postgresql'

    def build_testdb_connection_str(self) -> str:
        """Подключение к тестовой базе"""

        return URL.create(
            drivername=f'{self.database_system}+{self.driver}',
            username=self.user,
            database=self.test_name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)

    def build_connection_str(self) -> str:
        """This function build a connection string."""

        return URL.create(
            drivername=f'{self.database_system}+{self.driver}',
            username=self.user,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class AppConfig:
    """Bot configuration."""

    title = "MiniApp python hse"
    description = "Наше приложение"
    version = "1.0"
    root_path = ""


@dataclass
class Configuration:
    """All in one configuration's class."""

    debug: bool = bool(os.getenv('DEBUG'))
    logging_level: int = int(os.getenv('LOGGING_LEVEL', logging.INFO))
    yandex_api: YandexAPIConfig = field(default_factory=YandexAPIConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    app: AppConfig = field(default_factory=AppConfig)
    mongo_db: MongoDBConfig = field(default_factory=MongoDBConfig)
    s3: S3Config = field(default_factory=S3Config)
    auth_jwt: AuthJWTConfig = field(default_factory=AuthJWTConfig)

configuration = Configuration()
