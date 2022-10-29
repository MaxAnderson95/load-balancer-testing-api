import logging
import random
import string
from dynaconf import Dynaconf, Validator


def gen_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


settings = Dynaconf(
    envvar_prefix="API",
    settings_files=['settings.toml'],
    validators=[
        Validator("logging.level", default=logging.INFO),
        Validator("server.mode", default="API", is_in=["API","UI","FULL"]),
        Validator("server.port", default=80),
        Validator("server.instance_id", default=gen_id())
    ]
)
