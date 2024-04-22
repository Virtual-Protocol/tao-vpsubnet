import argparse
import asyncio
import bittensor as bt
from api.dummy import DummyAPI

"""
This is a sample of querying local bittensor subnet
Prerequisites:
1. Miner and validator are up and running

Expected output:
It will output whatever --input * 2 , 
eg: python virtualdemo.py --wallet_name validator --input 5
output: Results: [10]
"""


async def query_synapse(wallet_name, hotkey, network, netuid, input):
    # create a wallet instance with provided wallet name and hotkey
    wallet = bt.wallet(name=wallet_name, hotkey=hotkey)
    api = DummyAPI(wallet)

    metagraph = bt.metagraph(
        netuid=netuid, network=network, sync=True, lite=False
    )

    results = await api.query_api(metagraph.axons, dummy_input=input)
    print("Results: ", results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Query a Bittensor dummy synapse with given parameters."
    )

    # # Adding arguments
    parser.add_argument(
        "--netuid", type=int, default=1, help="Network Unique ID"
    )
    parser.add_argument(
        "--wallet_name", type=str, default="default", help="Name of the wallet"
    )
    parser.add_argument(
        "--hotkey", type=str, default="default", help="Hotkey for the wallet"
    )
    parser.add_argument(
        "--network",
        type=str,
        default="local",
        help='Network type, e.g., "local", "test" or "mainnet"',
    )
    parser.add_argument(
        "--input",
        type=int,
        default=1,
        help='Dummy input, expect the response to be input*2',
    )

    # # Parse arguments
    args = parser.parse_args()

    # Running the async function with provided arguments
    asyncio.run(
        query_synapse(
            args.wallet_name,
            args.hotkey,
            args.network,
            args.netuid,
            args.input,
        )
    )