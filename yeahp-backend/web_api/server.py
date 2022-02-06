from fastapi import FastAPI
from web_api.routers import hierarchy

app = FastAPI()

# Registers routers
app.include_router(hierarchy.router)
