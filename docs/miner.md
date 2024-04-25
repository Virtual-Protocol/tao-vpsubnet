# Miner
The role of the Miner is to provide motion animation given an audio input using an audio-to-animation model. This audio input prompt is provided by the Validator.

We reference open-source Audio-to-Animation models (MIT License), [EDGE](https://github.com/Stanford-TML/EDGE/tree/main) and [DiffuseStyleGestrue](https://github.com/YoungSeng/DiffuseStyleGesture). Please find respective model training documentation in the links provided. We provide updated documentation on setting up the development and inference environment for the EDGE model as reference [here](./EDGE/README.md). Note that these models and implementations are only references and submissions will be competitive. Miners will likely have to develop and innovate on such models either in the form of architectures or through collection and curation of data. Hence, Miners will also have to train custom models locally and publish their best model to 🤗 Hugging Face to be competitive.

The example build this repo was validated on:
 - Ubuntu 22.04
 - 64-bit Python 3.9
 - 50 GB HardDisk
 - 32 GB RAM
 - NVIDIA RTX 3090

# System Requirements
Miners will need disk space and compute power to both store the model as well as for inference and (optionally) train their model. It is recommended to have at least 50 GB of disk space and GPU with atleast 24 GB of VRAM for inference.

# Getting started
## Prerequisites

1. Conda environment ready `conda create -y -n edge python=3.9`
2. libsndfile package installed `sudo apt-get install libsndfile1`


## Installation and Environment Setup

1. Activate the Conda environment `conda activate edge`
2. Run the installation script `bash install.sh`
3. Download the SMPL body files (MALE, FEMALE, NEUTRAL) from https://smpl.is.tue.mpg.de/index.html and place them in directory vpa2a/smpl2bvh/data/smpl/smpl
