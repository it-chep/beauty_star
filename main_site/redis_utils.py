import logging

import redis
from django.conf import settings

logger = logging.getLogger(__name__)


def get_redis(broker_url=None, new_connect=False):
    client = getattr(get_redis, "client", None)
    if client and new_connect:
        client = None
    if client is None:
        pool = redis.ConnectionPool.from_url(broker_url or settings.BROKER_URL)
        client = redis.Redis(connection_pool=pool)
        get_redis.client = client
    return client


def get_redis_client(broker_url=None):
    broker_url = "redis://beauty-redis:6379"
    try:
        client = get_redis(broker_url)
        client.echo("test")
    except (redis.ConnectionError, redis.ResponseError) as e:
        print(redis.ConnectionError("Redis not available: {}".format(e)))
        return
    return client


REDIS_CLIENT = get_redis_client()
