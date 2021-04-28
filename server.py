""" Run a dev server hosting the application"""

import logging

import uvicorn

from src.config import get_config

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    env = get_config().environment
    logger.info(f"Attempting to start server in {env.value} mode")

    uvicorn.run(
        "src.api:create_api",
        factory=True,
        reload=True,
        log_config=None,
    )
