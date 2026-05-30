import os
from flask_caching import Cache

cache = Cache()


def init_cache(app):
    """Inicializa Redis como backend de cache."""
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = redis_url
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300
    cache.init_app(app)
