""" Entry point for the API"""

import logging
from functools import cached_property

from fastapi import FastAPI

from src.config import Config, get_config

from .routers import routers

logger = logging.getLogger(__name__)


class API(FastAPI):
    @cached_property
    def config(self) -> Config:
        return get_config()


def create_api() -> API:
    api = API()
    logger.info(f"Initialized API in {api.config.environment.value} mode")

    for router in routers:
        logger.info(f"Adding {router.name} at {router.prefix}")
        api.include_router(router.api_router, prefix=router.prefix)

    return api
