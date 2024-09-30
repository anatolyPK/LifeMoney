from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from core.config.project import settings
from core.middlewares import add_process_time_header
from routing.routes import get_apps_router
from utils.redis_manager import redis_client


def get_application() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # // TODO chto eto and how connect redis
        await redis_client.connect()
        redis = await redis_client.get_client()
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        yield
        await redis_client.close()

    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        lifespan=lifespan,
    )
    application.include_router(get_apps_router())
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.middleware("http")(add_process_time_header)

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
