
# EDGE Model Miner Reference Documentation

  

This provides updated documentation to setup the development and inference environment for miner using the [EDGE](https://github.com/Stanford-TML/EDGE/tree/main) model as reference. The example build this repo was validated on:
 - Ubuntu 22.04
 - 64-bit Python 3.9
 - 50 GB HardDisk
 - 32 GB RAM
 - NVIDIA RTX 3090
  

## Prerequisites

1. Conda environment ready `conda create -y -n edge python=3.9`
2. libsndfile package installed `sudo apt-get install libsndfile1`

## Installation and Environment Setup

1. Activate the Conda environment `conda activate edge`
2. Run the installation script `bash install.sh`