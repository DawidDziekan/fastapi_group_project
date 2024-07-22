import redis.asyncio as redis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_limiter import FastAPILimiter

from fastapi_app.src.routes import auth, users, comments, search_filter, photos
from fastapi_app.src.conf.config import settings

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(photos.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(search_filter.router, prefix="/api")


@app.on_event("startup")
async def startup():
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        db=0,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(r)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
