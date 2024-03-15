from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import DatabaseSettings, get_settings

_db_settings = get_settings(DatabaseSettings)

if _db_settings.mode == "TEST":
    DATABASE_PARAMS = {
        "poolclass": NullPool,
    }
elif _db_settings.mode in {"DEV", "PROD"}:
    DATABASE_PARAMS = {
        "pool_size": 20,
        "pool_pre_ping": True,
        "pool_use_lifo": True,
    }

async_engine = create_async_engine(
    url=_db_settings.url,
    echo=_db_settings.echo,
    # pool_size=20,
    # pool_pre_ping=True,
    # pool_use_lifo=True,
    **DATABASE_PARAMS,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
