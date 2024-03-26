import contextlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from settings import AppSettings, RedisSettings, get_settings

from .routers import router_ref_codes, router_users, router_users_auth

_app_settings = get_settings(AppSettings)
_redis_settings = get_settings(RedisSettings)


@contextlib.asynccontextmanager
async def _lifespan(app: FastAPI):  # noqa: ANN202, ARG001
    redis = aioredis.from_url(
        f"redis://{_redis_settings.host}:{_redis_settings.port}",
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    _include_routers(app)
    _add_middlewares(app)
    return app


def _include_routers(app: FastAPI) -> None:
    app.include_router(router_users)
    app.include_router(router_users_auth)
    app.include_router(router_ref_codes)


def _add_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_app_settings.allow_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=[
            "Content-Type",
            "Set-Cookie",
            "Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin",
            "Authorization",
        ],
    )
