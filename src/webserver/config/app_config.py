import logging
import os
from typing import Optional

from pydantic import Field, computed_field, NonNegativeInt, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from logging import getLogger

# 创建日志记录器
logger = getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
# 检查 .env 文件是否存在
env_path = os.path.join(os.getcwd(), '.env')
logger.info(f"文件路径：{env_path}")
logger.info(f"检查 .env 文件是否存在: {os.path.exists(env_path)}")
if os.path.exists(env_path):
    logger.info(f".env 文件内容: {open(env_path, 'r').read()}")
else:
    logger.warning(f".env 文件不存在于路径: {env_path}")


class DbConfig(BaseSettings):
    DB_HOST: str = Field(
      description="数据库ip",
      default="localhost",
    )
    DB_PORT: int = Field(
      description="数据库端口",
      default="3306",
    )
    DB_USERNAME: str = Field(
        description="数据库用户名",
        default="root",
    )
    DB_PASSWORD: str = Field(
        description="数据库密码",
        default="root",
    )
    DB_DATABASE: str = Field(
        description="数据库名",
        default="python_door",
    )
    DB_EXTRA: str = Field(
        description="数据库连接额外参数",
        default="",
    )
    DB_ENCODING: str = Field(
        description="数据库编码",
        default="utf8mb4",
    )
    SQLALCHEMY_DATABASE_URI_SCHEME: str = Field(
        description="Database URI scheme for SQLAlchemy connection.",
        default="",
    )
    @computed_field
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        db_extras: str = (
            f"{self.DB_EXTRA}&charset={self.DB_ENCODING}" if self.DB_ENCODING else self.DB_EXTRA
        ).strip("&")

        db_extras = f"?{db_extras}" if db_extras else ""
        uri = (
            f"{self.SQLALCHEMY_DATABASE_URI_SCHEME}://"
            f"{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
            f"{db_extras}"
        )
        logger.info(f"构建的数据库 URI: {uri}")
        return uri

    SQLALCHEMY_POOL_SIZE: NonNegativeInt = Field(
        description="Maximum number of database connections in the pool.",
        default=30,
    )

    SQLALCHEMY_MAX_OVERFLOW: NonNegativeInt = Field(
        description="Maximum number of connections that can be created beyond the pool_size.",
        default=10,
    )

    SQLALCHEMY_POOL_RECYCLE: NonNegativeInt = Field(
        description="Number of seconds after which a connection is automatically recycled.",
        default=3600,
    )

    SQLALCHEMY_POOL_PRE_PING: bool = Field(
        description="If True, enables connection pool pre-ping feature to check connections.",
        default=False,
    )

    SQLALCHEMY_ECHO: bool | str = Field(
        description="If True, SQLAlchemy will log all SQL statements.",
        default=False,
    )

    RETRIEVAL_SERVICE_EXECUTORS: NonNegativeInt = Field(
        description="Number of processes for the retrieval service, default to CPU cores.",
        default=os.cpu_count(),
    )


class LoggingConfig(BaseSettings):
    """
    Configuration for application logging
    """

    LOG_LEVEL: str = Field(
        description="Logging level, default to INFO. Set to ERROR for production environments.",
        default="INFO",
    )

    LOG_FILE: Optional[str] = Field(
        description="File path for log output.",
        default=None,
    )

    LOG_FILE_MAX_SIZE: PositiveInt = Field(
        description="Maximum file size for file rotation retention, the unit is megabytes (MB)",
        default=20,
    )

    LOG_FILE_BACKUP_COUNT: PositiveInt = Field(
        description="Maximum file backup count file rotation retention",
        default=5,
    )

    LOG_FORMAT: str = Field(
        description="Format string for log messages",
        default="%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)d] - %(message)s",
    )

    LOG_DATEFORMAT: Optional[str] = Field(
        description="Date format string for log timestamps",
        default=None,
    )

    LOG_TZ: Optional[str] = Field(
        description="Timezone for log timestamps (e.g., 'America/New_York')",
        default="UTC",
    )



## 继承底层配置类，然后统一使用SettingsConfigDict初始化读取.env配置文件
class DoorConfig(DbConfig, LoggingConfig,):
    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        # ignore extra attributes
        extra="ignore",
    )


    # Before adding any config,
    # please consider to arrange it in the proper config group of existed or added
    # for better readability and maintainability.
    # Thanks for your concentration and consideration.

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        logger.info("自定义配置来源")
        return (
            init_settings,
            env_settings,
            # RemoteSettingsSourceFactory(settings_cls),
            dotenv_settings,
            file_secret_settings,
        )

# 创建配置实例
door_config = DoorConfig()

# 输出配置信息以便调试
logger.info(f"加载的配置: {door_config.model_dump()}")

