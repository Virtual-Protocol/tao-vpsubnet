# Validator
The role of the Validator is to start animation generation by providing a audio-prompt that has a corresponding motion animation (audio-animation pair). The Validator will provide the audio-prompt to the Miner, who will generate the motion animation. The Validator will then evaluate the generated motion animation.

The validation mechanism will evolve in phases as the field matures and this subnet further develops. To start, Validators will select or sample audio-animation pairs from a library provided by the Subnet Provider. This library is obtained from real-world dances captured. The Subnet Provider will maintain and continue to add to this library to increase the diversity of audio-animation pairs used for validation. As the frontier of A2A field and models progress, Validators will be able to provide their own audio prompts (and not require this library) in  future validation and evaluation phases. This can potentially involved generating reference animations using a more powerful frontier models or using multi-modal visual language models as evaluators (i.e. AI feedback).


## Evaluation Protocol (Current Phase)
The evaluation protocol currently involves comparing the generated animation provided by the Miner with the reference animation. The evaluation will be based on the similarity of the generated animation with the reference animation. 

In future phases, more sophisticated and detailed metrics for motion evaluation can be added such as the PFC score for realism and syncing of motion and beats.
The motion animation from Miners and Validators can also be encoded where we can take the distance between motions in the embedding space.


## System Requirements
Currently, Validators do not need much disk space and compute power. GPUs are not required. However, in future evaluation protocols and validation phases, it is recommended to have at least 50 GB of disk space and GPU with atleast 24 GB of VRAM for inference.


## Running the validator

1. Set the **VALIDATOR_LIB** environment variable to validator audio library url
2. Run `bash scripts/start_validator.sh`
