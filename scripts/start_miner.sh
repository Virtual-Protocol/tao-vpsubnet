#!/bin/bash
export PYTHONPATH="$PWD:$PWD/vpa2a"
python neurons/miner.py --netuid 25 --subtensor.network finney --wallet.name miner --wallet.hotkey default --logging.debug