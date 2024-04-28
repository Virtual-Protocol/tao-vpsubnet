# Virtual Protocol's Audio-to-Animation (A2A) Subnet

---
- [Introduction](#introduction)
  - [Roadmap](#roadmap)
  - [Status](#status)
- [Mechanism](#mechanism)
  - [Evaluation Protocol](#validator)  
- [Getting Started](#started)
  - [Validator](#validator)
  - [Miner](#miner)
- [Acknowledgement](#acknowledgement)
- [License](#license)
---

## Introduction
Audio-to-Animation (A2A), also referred to as audio-driven animation, generates visuals that dynamically respond to audio inputs. This technology finds applications across a wide range of domains including gaming AI agents, livestreaming AI idols, virtual companions, metaverses, and more.

This Bittensor subnet offers a platform for democratizing the creation of an A2A model, gathering the help of the wider ML community in Bittensor to generate the best animated motions and bring life to the on-chain AI agents.

For more background info on why we need an A2A model, feel free to check out our [whitepaper] ().

### Roadmap
We will divide the development of the A2A model into several phases, with an iterative approach to make it better over time.

- **Phase 1**: Focus on generating full body motions, such as dance movements, based on the audio input on a specific curated dataset.
- **Phase 2**: Recognise the mood and genre of the audio input and adjust the generated animation accordingly.
- **Phase 3**: Expands models capabilities beyond dance audio and motions.
- **Phase 4**: Optimize models for real-time interaction capabilities.

### Status
Currently, we're at Phase 1, where audio-to-dance motions will be the focus. Validators will choose a prompt from the reference library and send the prompt to miners for generation of animation outputs.

## Mechanism
![mechanism] ()
1. **Subnet owner:** Virtual Protocol as the subnet owner, create the modules for miners and validators to train and evaluate the generated animation. Also decide the parameters required to evaluate the animation’s performance. 
2. **Miners:** Generate animations with A2A models using reference models or other models.
3. **Validators:** Provide audio prompts and evaluate the submitted animation from miners based on the parameters suggested by the subnet owner. 
4. **Bittensor protocol:** Aggregate weights using Yuma Consensus and determine the final weights and allocation ratios for each miner and validator.

### Evaluation Protocol
Given the non-determinism of an animation output, an evaluation mechanism which considers multiple parameters will be implemented in a phased approach. Read up more about the evaluation mechanism under Validator README. 

## Getting Started

### Validator
See [Validator documentation and guide](./docs/validator.md).

### Miner
See [Miner documentation and guide](./docs/miner.md).

## Acknowledgements
We would like to thank XX

## License
This repository is licensed under the MIT License.
```text
# The MIT License (MIT)
# Copyright © 2023 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```
