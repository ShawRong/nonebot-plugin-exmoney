#from nonebot import get_driver
from pydantic import BaseModel


class Config(BaseModel):
#    exchange_app_key: str
#    exchange_decimals: int = Field(2, ge=0)
    pass


#config = Config.parse_obj(get_driver().config)
