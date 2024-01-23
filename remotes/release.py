from loguru import logger

import asyncio
import aiohttp

from app_globals import app_config, current_massa_release
from tg_queue import send_telegram_message


@logger.catch
async def get_latest_massa_release(github_api_url: str=app_config['service']['github_api_url']) -> object:
    logger.debug("-> Enter Def")

    async with aiohttp.ClientSession() as session:

        try:
            async with session.get(url=github_api_url) as github_response:
                github_response_obj = await github_response.json()
            
            latest_release = github_response_obj['name']
            github_response_result = {"result": f"{latest_release}"}

        except Exception as E:
            logger.error(f"Exception in Github API request: ({str(E)})")
            github_response_result = {"error": f"Exception: ({str(E)})"}

        else:
            if github_response.status != 200:
                logger.error(f"Github API HTTP error: (HTTP {github_response.status})")
                github_response_result = {"error": f"HTTP Error: ({github_response.status})"}
        
        finally:
            return github_response_result




@logger.catch
async def release() -> None:
    logger.debug(f"-> Enter Def")

    global current_massa_release

    while True:

        await asyncio.sleep(delay=app_config['service']['main_loop_period_sec'])

        try:
            release_result = await get_latest_massa_release()
            latest_release = release_result['result']

        except Exception as E:
            logger.warning(f"Cannot get latest MASSA release version: ({str(E)}). Result: {release_result}")

        else:
            logger.info(f"Got latest MASSA release version: {latest_release}")

            if latest_release != current_massa_release:
                await send_telegram_message(message_text=f"📩 New MASSA version released:\n\n<pre>{current_massa_release} → {latest_release}</pre>")
            
            current_massa_release = latest_release




if __name__ == "__main__":
    pass
