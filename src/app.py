from config import config
from fastapi import FastAPI
from api.api_v1_0.routers import router as api_router_v1_0
from api.api_v1_0.endpoints.shortener import router as shortener_router
from starlette.middleware.cors import CORSMiddleware
import logging

app = FastAPI(title=config.app_title)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(api_router_v1_0, prefix='/api_v1.0')
app.include_router(shortener_router, prefix='/r', tags=["r"])

logging.basicConfig(level=config.log_level)
logging.info("application starts...")

if config.debug and __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
