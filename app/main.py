import uvicorn
import logging
import pkg_resources
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from config import settings
from logger import configure_logging
from util import gen_response, get_xff

logger = configure_logging(__name__)

app = FastAPI()

if settings.server.mode == "UI" or settings.server.mode == "FULL":
    app.mount("/static", StaticFiles(directory=pkg_resources.resource_filename(__name__, 'static')), name="static")

    @app.get("/", include_in_schema=False)
    def root():
        return HTMLResponse(pkg_resources.resource_string(__name__, 'static/index.html'))

if settings.server.mode == "UI":
    @app.get("/{full_path:path}")
    @app.head("/{full_path:path}")
    async def ui_health_monitor(request: Request, full_path: str):
        health_check = "health" in request.url.path
        if not health_check:
            raise HTTPException(status_code=404, detail="Not Found")
        else:
            return gen_response(request)

if settings.server.mode == "API":
    @app.get("/{full_path:path}")
    @app.head("/{full_path:path}")
    async def catch_all(request: Request, full_path: str):
        return gen_response(request)

if settings.server.mode == "FULL":
    @app.get("/api/{full_path:path}")
    @app.head("/api/{full_path:path}")
    @app.get("/actuator/{full_path:path}")
    @app.head("/actuator/{full_path:path}")
    async def catch_all(request: Request, full_path: str):
        return gen_response(request)


@app.middleware("http")
def log_requests(request: Request, call_next):
    if "health" in request.url.path:
        middleware_log_level = logging.DEBUG
    else:
        middleware_log_level = logging.INFO

    logger.log(middleware_log_level,
            f"INSTANCE: '{settings.server.instance_id}', METHOD: '{request.method}', PATH: '{request.url.path}' CLIENT: '{request.client.host}', XFF: '{get_xff(request)}'")
    response = call_next(request)
    return response


if __name__ == "__main__":
    logger.info(f"Launching server instance '{settings.server.instance_id}' on port '{settings.server.port}' in '{settings.server.mode}' mode.")
    logger.debug("DEBUG logging is enabled")
    uvicorn.run("main:app", host="0.0.0.0", port=int(settings.server.port), proxy_headers=False, log_level="critical")
