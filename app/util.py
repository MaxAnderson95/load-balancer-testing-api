from fastapi import Request
from config import settings


def get_xff(request: Request):
    return request.headers.get("X-Forwarded-For", default="Not Found")


def gen_response(request: Request, health_check: bool = False):
    response = {
        "Server Instance ID": settings.server.instance_id,
        "Client IP": request.client.host,
        "x-forwarded-for Header": get_xff(request),
        "Requested Path": request.url.path
    }

    if health_check:
        response["status"] = "UP"

    return response
