from functools import lru_cache
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, vote
from . import config


# models.Base.metadata.create_all(bind=database.engine)


@lru_cache()
def get_settings() -> config.Settings:
    return config.Settings()


app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Deployed from CI/CD pipeline"}
