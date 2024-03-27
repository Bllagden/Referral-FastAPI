from celery import Celery

from settings import RedisSettings, get_settings

_redis_settings = get_settings(RedisSettings)

celery_app = Celery(
    "tasks",
    broker=f"redis://{_redis_settings.host}:{_redis_settings.port}",
    include=[
        "adapters.celery.tasks",
    ],
)
