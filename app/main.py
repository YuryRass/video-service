from fastapi import FastAPI

from app.handlers import routers

app = FastAPI(title="Video service application")


for router in routers:
    app.include_router(router)
