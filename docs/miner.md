# Miner
The role of the Miner is to provide motion animation given an audio input using an audio-to-animation model. This audio input prompt is provided by the Validator.

We reference open-source Audio-to-Animation models (MIT License), [EDGE](https://github.com/Stanford-TML/EDGE/tree/main) and [DiffuseStyleGesture](https://github.com/YoungSeng/DiffuseStyleGesture). Please find respective model training documentation in the links provided. To easily get started, we provide a functioning miner setup as well as updated documentation for the inference using the EDGE model as reference below. Note that these models and implementations are only references and submissions will be competitive. Miners will likely have to develop and innovate on such models either in the form of architectures, training procedures or through collection and curation of data. Hence, Miners will potentially also have to train custom models locally and use these models.

The example build this repo was validated on:
 - Ubuntu 22.04
 - 64-bit Python 3.9
 - NodeJS v21
 - 50 GB HardDisk
 - 32 GB RAM
 - NVIDIA RTX 3090

# System Requirements
Miners will need disk space and compute power to both store the model as well as for inference and (optionally) train their model. It is recommended to have at least 50 GB of disk space and GPU with 16 GB of VRAM for inference.

# Getting started
## Prerequisites

1. Conda environment ready `conda create -y -n vpa2a python=3.9`
2. libsndfile package installed `sudo apt-get install libsndfile1`


## Installation and Environment Setup

1. Activate the Conda environment `conda activate vpa2a`
2. Run the installation script `bash install.sh`
3. Download the SMPL body files (MALE, FEMALE, NEUTRAL) from https://smpl.is.tue.mpg.de/index.html and place them in directory vpa2a/smpl2bvh/data/smpl/smpl

## Running the Miner

1. Activate the Conda environment `conda activate vpa2a`
2. Start up the inferencing API service for the A2A model `bash scripts/start_api.py`
3. Run `bash scripts/start_miner.sh`
