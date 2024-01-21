import aiohttp
from loguru import logger
from aiogram.enums import ParseMode
from init import app_settings, tg_bot



@logger.catch
async def pull_node_api(
        api_url: str="",
        api_header: object={"content-type": "application/json"},
        api_payload: object={},
        api_timeout: int=app_settings['probe_timeout_seconds']) -> object:
    logger.debug(f"-> Enter def")

    api_timeout = aiohttp.ClientTimeout(total=api_timeout)
    async with aiohttp.ClientSession() as session:

        try:
            api_response = await session.post(url=api_url,
                                              headers=api_header,
                                              data=api_payload,
                                              timeout=api_timeout)
            api_response_obj = await api_response.json()
            api_response_result = api_response_obj['result']

        except Exception as E:
            logger.error(f"Exception in API request for URL '{api_url}': ({str(E)})")
            api_response_result = {"error": f"Exception: ({str(E)})"}

        else:
            if api_response.status != 200:
                logger.error(f"API URL '{api_url}' response status error: (HTTP {api_response.status})")
                api_response_result = {"error": f"HTTP Error: ({api_response.status})"}

    return api_response_result




@logger.catch
async def send_telegram_message(message_text: str="") -> None:
    logger.debug(f"-> Enter def")

    try:
        await tg_bot.send_message(chat_id=app_settings['telegram']['chat_id'], text=f"{app_settings['telegram']['service_nickname']}:\n\n{message_text}", parse_mode=ParseMode.HTML)
    
    except Exception as E:
        logger.warning(f"Cannot send telegram message to chat_id '{app_settings['telegram']['chat_id']}': ({str(E)})")

    else:
        logger.info(f"Successfully sent telegram message to chat_id '{app_settings['telegram']['chat_id']}'")

    return




@logger.catch
async def get_nodes_text() -> str:
    logger.debug(f"-> Enter def")

    nodes_list = ""
    for node_name in app_settings['nodes']:
        node_url = app_settings['nodes'][node_name]['url']
        node_num_wallets = len(app_settings['nodes'][node_name]['wallets'])
        nodes_list += f" • {node_name}: {node_url} - {node_num_wallets} wallet(s)\n"

    if nodes_list == "":
        return "⭕ Nodes list is emtpy.\n\n➡ Use /help to learn how to add a node to watch."
    else:
        return nodes_list.rstrip()




if __name__ == "__main__":
    pass