import requests
from fastapi import Request
from config import settings


def get_xff(request: Request):
    return request.headers.get("X-Forwarded-For", default="Not Found")


def gen_response(request: Request):
    response = {
        "server_details": {
            "server_instance_id": settings.server.instance_id,
            "server_mode": settings.server.mode,
            "server_listening_port": settings.server.port,
        },
        "request_details": {
            "client_ip": request.client.host,
            "x-forwarded-for_header": get_xff(request),
            "request_path": request.url.path
        },
    }

    if "health" in request.url.path:
        response["status"] = "UP"

    if "joke" in request.url.path:
        joke_response = requests.get("https://official-joke-api.appspot.com/random_joke")
        try:
            joke_response.raise_for_status()
        except:
            response["joke"] = "FAILED TO RETREIVE JOKE FROM EXTERNAL API"
        else:   
            response["joke"] = joke_response.json()
        

    return response
