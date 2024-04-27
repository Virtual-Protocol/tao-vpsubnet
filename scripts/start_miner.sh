#!/bin/bash
export PYTHONPATH="$PWD:$PWD/vpa2a:$PWD/vpa2a/EDGE:$PWD/vpa2a/smpl2bvh"
python neurons/miner.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9944 --wallet.name miner --wallet.hotkey default --logging.debug