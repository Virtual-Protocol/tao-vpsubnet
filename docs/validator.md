# Validator
The role of the Validator is to start animation generation by providing a audio-prompt. The Validator will provide the audio-prompt to the Miner, who will generate the motion animation. The Validator will then evaluate the generated motion animation.

The validation mechanism will evolve in phases as the field matures and this subnet further develops. To start, Validators will select or sample audio-animation pairs from a library provided by the Subnet Owner. This library is obtained from real-world dances captured. The Subnet Onwer will maintain and continue to add to this library to increase the diversity of audio-animation pairs used for validation. As the frontier of A2A field and models progress, Validators will be able to provide their own audio prompts (and not require this library) in  future validation and evaluation phases. This can potentially involve generating reference animations using a more powerful frontier models or using multi-modal visual language models as evaluators (i.e. AI feedback).


## Evaluation Protocol (Current Phase)
The evaluation protocol currently involves comparing the generated animation provided by the Miner with the reference animation. The evaluation will be based on the similarity of the generated animation with the reference animation as well as the response speed.

*Root Mean Square Error (RMSE)*

To evaluate similarity in motion data, we currently compute the Root Mean Square Error (RMSE) between animations. This method involves comparing two sets of motion data: the generated data and the reference data collected from real-world data. The process starts by aligning these two datasets in time and space, ensuring that they correspond to the same motion events and timelines. Each corresponding pair of data points (i.e., generated vs. reference) is then used to compute the differences, which are subsequently averaged over the entire trajectory. The RMSE is finally obtained by taking the square root of this average, providing a single value that quantifies the average magnitude of the error between the generated and reference motion data. This metric is particularly valuable because it provides a clear and direct measure of the prediction accuracy, with lower values indicating better model performance. This RSME contributes to the 'correctness score' part of the evaluation. 

*Response Speed*
Speed is a measure of how fast the miners respond to the validator requests. Speed is measured as function of the ratio of miner response time against the internal max_response_time that is set by the owners, which is determined through continuous testing with miners of various compute specs, as well as through gauging the frequency of demand from users. A score is given through this function, and is the 'speed score' part of the evaluation. 

The combined score is a function of both scoring types. The speed score has a slightly lower weightage compared to the correctness score on the combined score for a miner response. 

## System Requirements
Currently, Validators do not need much disk space and compute power. GPUs are not required. However, in future evaluation protocols and validation phases, it is recommended to have at least 50 GB of disk space and GPU with atleast 24 GB of VRAM for inference.


## Running the validator

1. Set the **VALIDATOR_LIB** environment variable to validator audio library url
2. Run `bash scripts/start_validator.sh`
