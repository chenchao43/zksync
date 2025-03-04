from typing import Awaitable
from utils.runner import *
from colorama import Fore
from loguru import logger
from tqdm import tqdm
from web3 import Web3
from config import *
import random
import sys

from asyncio import (
    create_task,
    gather,
    run,
    sleep,
)



def load_module_config():
    with open('config.py', 'r', encoding='utf-8-sig') as file:
        module_config = file.read()
    exec(module_config)

print(f'----------------------------------------Modules--------------------------------------------')

def get_activate_module():

    module_handlers = {
    'orbiter_bridging': process_orbiter_bridging,
    'inch_swap': process_inch_swap,
    'bungee_bridge': process_bungee_bridge,
    'syncswap_swap': process_sync_swap_swap,
    'syncswap_liq': process_sync_swap_liquidity,
    'mute_swap': process_mute_swap,
    'mute_liq': process_mute_liq,
    'main_bridge': process_main_bridge,
    'nft_domain_service': process_nft_domain_service,
    'nft_mint_and_bridge': process_nft_mint_and_bridge,
    'spacefi_swap': process_spacefi_swap,
    'spacefi_liq': process_spacefi_liq
    }

    patterns = {}

    for module in module_handlers:
        if globals().get(module):
            patterns[module] = 'On'
        else:
            patterns[module] = 'Off'

    for pattern, value in patterns.items():
        if value == 'Off':
            print("\033[31m {}".format(f'{pattern} = {value}'))
        else:
            print("\033[32m {}".format(f'{pattern} = {value}'))
    print('\033[39m')

    active_module = [module for module, value in patterns.items() if value == 'On']
    return active_module,module_handlers


async def main() -> None:
    tasks = []

    for private_key in private_keys:
        if RANDOMIZE is False:
            for pattern in active_module:
                task = create_task(module_handlers[pattern](private_key, pbar))
                tasks.append(task)
            time_to_sleep = SLEEP_TIME
            logger.info(f'Sleeping {time_to_sleep} seconds...')
            await sleep(time_to_sleep)

        else:
            random.shuffle(active_module)
            for pattern in active_module:
                task = create_task(module_handlers[pattern](private_key, pbar))
                tasks.append(task)
                time_to_sleep = SLEEP_TIME
                logger.info(f'Sleeping {time_to_sleep} seconds...')
                await sleep(time_to_sleep)

    await gather(*tasks)


def start_event_loop(awaitable: Awaitable[object]) -> None:
    run(awaitable)


if __name__ == '__main__':
    
    active_module,module_handlers = get_activate_module()

    with open('wallets.txt', 'r', encoding='utf-8-sig') as file:
        private_keys_all = [line.strip() for line in file]

    for account_num in [int(sys.argv[1])]:
        
        load_module_config()
        web3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
        private_keys = [private_keys_all[account_num]]

        for private_key in private_keys:
            print(web3.eth.account.from_key(private_key).address)
        with tqdm(total=len(private_keys)) as pbar:
            async def tracked_main():
                await main()

            start_event_loop(tracked_main())
