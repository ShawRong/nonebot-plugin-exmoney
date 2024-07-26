from datetime import datetime
from typing import Dict, List, Tuple

import httpx
from nonebot import require
from nonebot.log import logger
from pydantic import BaseModel

from .config import config

from bocfx import bocfx

require("nonebot_plugin_apscheduler")

#currency_dict: Dict[str, Tuple[str, ...]] = {
#    "澳大利亚元": ("澳元",),
#    "加拿大元": ("加元", "加币"),
#    "瑞士法郎": ("法郎",),
#    "丹麦克朗": (),
#    "欧元": (),
#    "英镑": (),
#    "港币": ("港元", "香港元"),
#    "印尼卢比": (),
#    "日元": ("円", "日圆"),
#    "韩元": ("韩币",),
#    "澳门元": ("澳币", "澳门币"),
#    "挪威克朗": (),
#    "新西兰元": (),
#    "菲律宾比索": ("比索",),
#    "卢布": ("俄元",),
#    "瑞典克朗": (),
#    "新加坡元": (),
#    "泰国铢": ("泰铢",),
#    "土耳其里拉": (),
#    "美元": ("美刀",),
#    "南非兰特": (),
#}

#this class is for storing the data got by bocfx.
class ExchangeRate(BaseModel):
    """name for currency"""
    name: str
    """spot exchange bid"""
    se_bid: float
    """bid for bonds"""
    bn_bid: float
    """spot exchange ask"""
    se_ask: float
    """ask for bonds"""
    bn_ask: float
    """bank of china conversion rate"""
    boc_conv: float
    """time that bank of china released this price"""
    time: datetime

    def __str__(self) -> str:
        return (
            f"货币名称: {self.name}\n"
            f"现汇买入价 (SE_BID): {self.se_bid}\n"
            f"债券买入价 (BN_BID): {self.bn_bid}\n"
            f"现汇卖出价 (SE_ASK): {self.se_ask}\n"
            f"债券卖出价 (BN_ASK): {self.bn_ask}\n"
            f"中国银行转换率 (BOC_CONV): {self.boc_conv}\n"
            f"发布时间: {self.time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
    
    def name(self) -> str:
        return self.name
    
    def time(self) -> datetime:
        return self.time
    

#fields = ExchangeRate.model_fields.keys()
#exchange_dict: Dict[str, ExchangeRate] = {}

update_time = ""
# i dont this this dict is really necessary
currency2price = Dict(str, ExchangeRate)

def fetch_exchange(app_key: str) -> None:
    # fixme
    # i will use hkd for example
    # need to generalize it.
    # app_key should be modified and used
    hkd = bocfx(FX='HKD')
    # hkd_price example: ('HKD', '92.77', '92.02', '93.12', '93.12', '91.3', '2024-07-27 00:09:02')
    # hkd[1] equals to the up-to-date price
    hkd_price = hkd[1]
    # now hkd_price become a class
    hkd_price = ExchangeRate(**hkd_price)

    #store hkd(or something else) to currency2price str to class ExchangeRate
    #fixme: I dont think this logic is good enough
    global currency2price
    currency_name = hkd_price.name()
    currency2price[currency_name] = hkd_price

    #update the time
    #fixme: is this update time really necessary?
    global update_time
    update_time = hkd_price.time()

    logger.debug(f"汇率更新成功! 更新时间: {update_time}")
    

def get_exchange_rate(currency_name: str) -> ExchangeRate:
    try:
        return currency2price[currency_name]
    except KeyError:
#        for k, v in currency2price.items():
#            if currency_name in v:
#                return exchange_dict[k]
        raise ValueError("we did not get what you want, wrong currency or excluded from the database")

#implement: def exchange():

def get_currency_info(currency_name: str) -> str:
    er = get_exchange_rate(currency_name)
    return str(er)

#implement:
#def get_currency_list() -> List[str]:
#    return list(exchange_dict.keys())
