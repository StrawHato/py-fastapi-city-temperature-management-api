from fastapi import FastAPI

from dependencies import lifespan
from city import city_router

app = FastAPI(lifespan=lifespan)
app.include_router(city_router.router)
