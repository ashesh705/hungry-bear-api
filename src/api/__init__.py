""" Entry point for the API"""

import logging

from fastapi import FastAPI

from src.config import get_config

from .routers import routers

logger = logging.getLogger(__name__)


def create_api() -> FastAPI:
    api = FastAPI()

    config = get_config()
    logger.info(f"Initialized API in {config.environment.value} mode")

    for router in routers:
        logger.info(f"Adding {router.name} at {router.prefix}")
        api.include_router(router.api_router, prefix=router.prefix)

    return api
