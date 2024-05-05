# Validator
The role of the Validator is to start animation generation by providing a audio-prompt. The Validator will provide the audio-prompt to the Miner, who will generate the motion animation. The Validator will then evaluate the generated motion animation.

The validation mechanism will evolve in phases as the field matures and this subnet further develops. To start, Validators will select or sample audio-animation pairs from a library provided by the Subnet Owner. This library is obtained from real-world dances captured. The Subnet Onwer will maintain and continue to add to this library to increase the diversity of audio-animation pairs used for validation. As the frontier of A2A field and models progress, Validators will be able to provide their own audio prompts (and not require this library) in  future validation and evaluation phases. This can potentially involve generating reference animations using a more powerful frontier models or using multi-modal visual language models as evaluators (i.e. AI feedback).


## Evaluation Protocol (Current Phase)
The evaluation protocol currently involves comparing the generated animation provided by the Miner with the reference animation. The evaluation will be based on the similarity of the generated animation with the reference animation AS WELL AS SPEED.

*Root Mean Square Error (RMSE)*

To evaluate similarity in motion data, we currently compute the Root Mean Square Error (RMSE) between animations. This method involves comparing two sets of motion data: the generated data and the reference data collected from real-world data. The process starts by aligning these two datasets in time and space, ensuring that they correspond to the same motion events and timelines. Each corresponding pair of data points (i.e., generated vs. reference) is then used to compute the differences, which are subsequently averaged over the entire trajectory. The RMSE is finally obtained by taking the square root of this average, providing a single value that quantifies the average magnitude of the error between the generated and reference motion data. This metric is particularly valuable because it provides a clear and direct measure of the prediction accuracy, with lower values indicating better model performance.

*Speed*


## System Requirements
Currently, Validators do not need much disk space and compute power. GPUs are not required. However, in future evaluation protocols and validation phases, it is recommended to have at least 50 GB of disk space and GPU with atleast 24 GB of VRAM for inference.

Minimum requirements:
- 2 cores CPU
- 16 GB RAM
- 30 GB harddisk

# Getting started
## Prerequisites

1. Python 3.11
2. NodeJS v21
3. Register your Bittensor wallet as validator on netuid 25 and stake at least 100 TAO. In this example, we assume your wallet coldkey is *validator* and hotkey is *default*

## Installation and Environment Setup

1. Install PM2 process manager `sudo npm install -g pm2`
2. Install Python3.11 venv module `sudo apt install python3.11-venv`
3. Create a Python virtual environment `python3 -m venv venv`
4. Activate the virtual environment `source venv/bin/activate`
5. Run `pip install -r requirements.txt`

## Running the validator

1. Activate the virtual environment `source venv/bin/activate`
2. Run `pm2 start scripts/start_validator.sh --name validator`
3. To view the outputs, run `pm2 logs validator`
