import uvicorn
import logging
from fastapi import FastAPI, Request
from config import settings
from logger import configure_logging
from util import gen_response, get_xff

logger = configure_logging(__name__)

app = FastAPI()


@app.get("/{full_path:path}")
@app.head("/{full_path:path}")
async def catch_all(request: Request, full_path: str):
    health_check = "health" in request.url.path
    return gen_response(request, health_check)


@app.middleware("http")
def log_requests(request: Request, call_next):
    if "health" in request.url.path:
        middleware_log_level = logging.DEBUG
    else:
        middleware_log_level = logging.INFO

    logger.log(middleware_log_level,
               f"METHOD: '{request.method}', PATH: '{request.url.path}' CLIENT: '{request.client.host}', XFF: '{get_xff(request)}'")
    response = call_next(request)
    return response


if __name__ == "__main__":
    logger.info(f"Launching server instance '{settings.server.instance_id}' on port '{settings.server.port}'")
    logger.debug("DEBUG logging is enabled")
    uvicorn.run("main:app", host="0.0.0.0", port=int(settings.server.port), proxy_headers=False, log_level="critical")
