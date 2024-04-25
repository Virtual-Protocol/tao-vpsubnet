# Validator
The role of the Validator is to start animation generation by providing an audio-prompt that has a corresponding motion animation (audio-animation pair). The Validator will provide the audio-prompt to the Miner, who will generate the motion animation. The Validator will then evaluate the generated motion animation.

The validation mechanism will evolve in phases as the field matures and this subnet further develops. To start, Validators will select or sample audio-animation pairs from a library provided by the Subnet Provider. The Subnet Provider will continue to update and increase the diversity of audio-animation prompts in the library. In future phases, Validators will be able to provide their own audio prompts and potentially generate reference animations using a more powerful model or run multi-modal visual language models as evaluators (i.e. AI feedback).


## Evaluation Protocol
The evaluation protocol involves taking comparing the generated animation provided by the Miner with the reference animation. The evaluation will be based on the similarity of the generated animation with the reference animation. The evaluation will be based on the following metrics:



We can encode the entire motion and take the distance in the embedding space.


## System Requirements
Currently, Validators do not need much will need disk space and compute power. However, in future evaluation protocols and validation phases, it is recommended to have at least 50 GB of disk space and GPU with atleast 24 GB of VRAM for inference.


