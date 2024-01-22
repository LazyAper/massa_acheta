from loguru import logger

import json
from time import time as t_now

from app_init import app_results
from tools import send_telegram_message, pull_node_api


@logger.catch
async def check_node(node_name: str="") -> None:
    logger.debug(f"-> Enter Def")

    payload = json.dumps({
        "id": 0,
        "jsonrpc": "2.0",
        "method": "get_status",
        "params": []
    })

    try:
        node_result = await pull_node_api(api_url=app_results[node_name]['url'], api_payload=payload)
        node_chain_id = node_result['chain_id']
        node_chain_id = int(node_chain_id)

    except Exception as E:
        logger.warning(f"Node '{node_name}' ({app_results[node_name]['url']}) seems dead! ({str(E)})")

        if app_results[node_name]['last_status'] != False:
            app_results[node_name]['last_status'] = False
            await send_telegram_message(message_text=f"🏠  Node '<b>{node_name}</b>' ({app_results[node_name]['url']})\n\n☠  Seems dead or unavailable!\n\n<code>💻  {node_result}</code>\n\n⚠  Check node status or firewall settings.")

    else:
        logger.info(f"Node '{node_name}' ({app_results[node_name]['url']}) seems online!")

        if app_results[node_name]['last_status'] != True:
            app_results[node_name]['last_status'] = True
            app_results[node_name]['last_update'] = t_now()
            await send_telegram_message(message_text=f"🏠  Node '<b>{node_name}</b>' ({app_results[node_name]['url']})\n\n🌿  Become alive with Chain ID:\n\n<pre>{node_chain_id}</pre>")

    finally:
        logger.debug(f"API result for node '{node_name}' ({app_results[node_name]['url']}):\n{json.dumps(obj=node_result, indent=4)}")

        app_results[node_name]['last_result'] = node_result
    
    return




if __name__ == "__main__":
    pass
