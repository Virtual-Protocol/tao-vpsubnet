# Validator
The role of the Validator is to start animation generation by providing a audio-prompt. The Validator will provide the audio-prompt to the Miner, who will generate the motion animation. The Validator will then evaluate the generated motion animation.

The validation mechanism will evolve in phases as the field matures and this subnet further develops. To start, Validators will select or sample audio-animation pairs from a library provided by the Subnet Owner. This library is obtained from real-world dances captured. The Subnet Onwer will maintain and continue to add to this library to increase the diversity of audio-animation pairs used for validation. As the frontier of A2A field and models progress, Validators will be able to provide their own audio prompts (and not require this library) in  future validation and evaluation phases. This can potentially involve generating reference animations using a more powerful frontier models or using multi-modal visual language models as evaluators (i.e. AI feedback).


## Evaluation Protocol (Current Phase)
The evaluation protocol currently involves comparing the generated animation provided by the Miner with the reference animation. The evaluation will be based on the similarity of the generated animation with the reference animation AS WELL AS SPEED.

*Root Mean Square Error (RMSE)*

To evaluate motion data effectively, one common methodology employed is the computation of the Root Mean Square Error (RMSE). This method involves comparing two sets of motion data: the predicted or simulated data and the observed or actual data collected from sensors or real-world observation. The process starts by aligning these two datasets in time and space, ensuring that they correspond to the same motion events and timelines. Each corresponding pair of data points (i.e., predicted vs. observed) is then used to compute the squared differences, which are subsequently averaged over the entire dataset. The RMSE is finally obtained by taking the square root of this average, providing a single value that quantifies the average magnitude of the error between the predicted and actual motion data. This metric is particularly valuable because it provides a clear and direct measure of the prediction accuracy, with lower values indicating better model performance.

*Speed*
XX

## System Requirements
Currently, Validators do not need much disk space and compute power. GPUs are not required. However, in future evaluation protocols and validation phases, it is recommended to have at least 50 GB of disk space and GPU with atleast 24 GB of VRAM for inference.


## Running the validator

1. Set the **VALIDATOR_LIB** environment variable to validator audio library url
2. Run `bash scripts/start_validator.sh`
