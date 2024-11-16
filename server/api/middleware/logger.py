from fastapi import Request
from server.config.logger_config import logger


async def log_middleware(request: Request, call_next):
    """
    Middleware function that logs every endpoint connected to and then returns that endpoint.
    """
    log_dict = {"url": request.url.path, "method": request.method}

    logger.info(log_dict)

    response = await call_next(request)
    return response
