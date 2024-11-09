from pydantic import BaseModel, ValidationError
from console import console
import sys
import json

class EmailConfig(BaseModel):
    user: str
    password: str


class Config(BaseModel):
    server: str
    ssl: bool
    emails: list[EmailConfig]


def get_config() -> Config:
    try:
        with open("config.json") as f:
            return Config(**json.load(f))
    except ValidationError:
        console.print_exception()
        sys.exit(1)
    except FileNotFoundError:
        console.log("[red]找不到配置文件 [yellow]config.json")
        sys.exit(1)


config = get_config()