#!/bin/bash
export PYTHONPATH="$PWD:$PWD/vpa2a"
python neurons/validator.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9944 --wallet.name validator --wallet.hotkey default --logging.debug