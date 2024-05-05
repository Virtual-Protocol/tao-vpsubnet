#!/bin/bash
export PYTHONPATH="$PWD:$PWD/vpa2a"
export VALIDATOR_LIB=https://gyupnvds3t.ap-southeast-1.awsapprunner.com/challenges
python neurons/validator.py --netuid 25 --subtensor.network finney --wallet.name validator --wallet.hotkey default --logging.debug
