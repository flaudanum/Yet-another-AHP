import uvicorn
from fastapi import FastAPI
from web_api.routers import hierarchy

app = FastAPI()

# Registers routers
app.include_router(hierarchy.router)

if __name__ == '__main__':
    uvicorn.run("web_api.server:app", host="127.0.0.1", port=8000, log_level="info")

