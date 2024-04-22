# Miner
The role of the Miner is to provide motion animation given an audio input using an audio-to-animation model. This audio input prompt is provided by the Validator.

We reference open-source Audio-to-Animation models (MIT License), [EDGE](https://github.com/Stanford-TML/EDGE/tree/main) and [DiffuseStyleGesture](https://github.com/YoungSeng/DiffuseStyleGesture). Please find respective model training documentation in the links provided. We provide updated documentation on setting up the development and inference environment for the EDGE model as reference [here](./EDGE/README.md). Note that these models and implementations are only references and submissions will be competitive. Miners will likely have to develop and innovate on such models either in the form of architectures or through collection and curation of data. Hence, Miners will also have to train custom models locally and publish their best model to 🤗 Hugging Face to be competitive.


# System Requirements
Miners will need disk space and compute power to both store the model as well as for inference and (optionally) train their model. It is recommended to have at least 50 GB of disk space and GPU with atleast 24 GB of VRAM for inference.

# Getting started
## Prerequisites

