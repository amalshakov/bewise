from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.database import init_db
from app.my_kafka import start_kafka_producer, stop_kafka_producer
from app.routers.applications import router as applications_router
from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await start_kafka_producer()
    yield
    await stop_kafka_producer()


app = FastAPI(
    lifespan=lifespan,
    title="Application Processing Service",
)

app.include_router(
    applications_router,
    prefix="/applications",
    tags=["Applications"],
)

def main():
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
    )


if __name__ == "__main__":
    main()
