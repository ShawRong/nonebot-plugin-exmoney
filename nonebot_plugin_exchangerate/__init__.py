from datetime import datetime

from .config import config
from nonebot import on_command, on_endswith
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import Endswith
from nonebot_plugin_saa import AggregatedMessageFactory, Text
from nonebot.log import logger

from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

from .exchangerate import get_currency_info, fetch_exchange

#exchange = on_regex(r"(?P<amount>^\d+\.?\d*)(?P<currency>[\u4e00-\u9fff]{1,5}$)")
#@exchange.handle()
#async def _(matched: Dict[str, Any] = RegexDict()) -> None:
#    with contextlib.suppress(ValueError):
#        total = exchange_currency(matched["currency"], float(matched["amount"]))
#        msg = f"{total}人民币"
#        await exchange.send(msg, reply_message=True)

help = on_command("exchange rate help")
@help.handle()
async def _():
    help_msg = AggregatedMessageFactory([
        Text("""exchange rate: for show the lated exchange rate.""")
    ])
    await help_msg.finish()

info = on_endswith("exchange rate")
@info.handle()
async def _(event: MessageEvent, suffix: str = Endswith()) -> None:
    txt = event.get_plaintext()
    try:
        currency = txt[: -len(suffix)]
        if len(currency) > 5:
            return
        msg = get_currency_info(currency)
    except ValueError as e:
        msg: str = str(e)
    await info.send(msg)

@scheduler.scheduled_job(
    "interval",
    minutes=5,
    args=[config.exchange_app_key],
    next_run_time=datetime.now(),
    misfire_grace_time=30,
)
async def _(app_key: str) -> None:
    try:
        #fixme generalize app_key
        app_key = "HKD"
        msg = get_currency_info(app_key)
    except ValueError as e:
        msg: str = str(e)
    output = AggregatedMessageFactory(
        [Text(msg)]
    )
    await output.finish()

@scheduler.scheduled_job(
    "interval",
    minutes=5,
    args=[config.exchange_app_key],
    next_run_time=datetime.now(),
    misfire_grace_time=30,
)
async def _(app_key: str) -> None:
    update_time =  await fetch_exchange(app_key)
    logger.debug(f"exchange rate updated! the latest price release time: {update_time}")

#statement = on_fullmatch(("货币列表", "汇率列表"))
#@statement.handle()
#async def _() -> None:
#    currency_list = get_currency_list()
#    msg = "支持查询的货币:\n" + "\n".join(currency_list)
#    await statement.send(msg)
