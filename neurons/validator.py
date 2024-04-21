# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

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


import time

# Bittensor
import bittensor as bt

# Bittensor Validator Template:
import template
from template.validator import forward

# import base validator class which takes care of most of the boilerplate
from template.base.validator import BaseValidatorNeuron

import numpy as np


def read_bvh(file_path: str) -> np.ndarray:
    '''
    Read a BVH file and return the motion data as a numpy array (frame_count, channel_count)

    Args: 
        file_path: file path to a BVH file

    Returns: 
        motion data in the form of a numpy array
    '''
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Locate the beginning of the motion data                                                                                                                                                             
    motion_start = lines.index('MOTION\n')
    frames_line = lines[motion_start + 1]
    frame_count = int(frames_line.split()[1])

    # Locate the line where the frame time is defined and the actual motion data starts                                                                                                                   
    frame_time_line = motion_start + 2
    motion_data_start = frame_time_line + 1

    # Number of channels can be estimated from the number of columns in the first frame of motion data                                                                                                    
    channel_count = len(lines[motion_data_start].split())

    # Create an array to store the motion data                                                                                                                                                            
    motion_data = np.zeros((frame_count, channel_count))

    # Fill the array with motion data                                                                                                                                                                     
    for i in range(frame_count):
        frame_data = np.array(list(map(float, lines[motion_data_start + i].split())))
        motion_data[i] = frame_data

    return motion_data


def compute_pose_differences(bvh_file1: str, bvh_file2: str) -> float:
    '''
    Returns a single scalar value as difference between 2 motion animations (BVH files)
    '''
    # Read the BVH files - shape = (frame_count, anim_dim_count)                                                                                                                                                                                                                                                    
    data1 = read_bvh(bvh_file1)
    data2 = read_bvh(bvh_file2)

    # Check for the same number of frames and channels                                                                                                                                                                                                                      
    if data1.shape == data2.shape:
        err = data1 - data2
        mse = np.mean(np.square(err), axis=-1) # (frame_count,) mse over dimensions of each frame of animaition                                                                                                                                                            
        return np.mean(mse) # scalar - average mse over entire trajectory
    else:
        raise ValueError("BVH files do not have the same number of frames or channels")



class Validator(BaseValidatorNeuron):
    """
    Your validator neuron class. You should use this class to define your validator's behavior. In particular, you should replace the forward function with your own logic.

    This class inherits from the BaseValidatorNeuron class, which in turn inherits from BaseNeuron. The BaseNeuron class takes care of routine tasks such as setting up wallet, subtensor, metagraph, logging directory, parsing config, etc. You can override any of the methods in BaseNeuron if you need to customize the behavior.

    This class provides reasonable default behavior for a validator such as keeping a moving average of the scores of the miners and using them to set weights at the end of each epoch. Additionally, the scores are reset for new hotkeys at the end of each epoch.
    """

    def __init__(self, config=None):
        super(Validator, self).__init__(config=config)

        bt.logging.info("load_state()")
        self.load_state()

        # TODO(developer): Anything specific to your use case you can do here

    async def forward(self):
        """
        Validator forward pass. Consists of:
        - Generating the query
        - Querying the miners
        - Getting the responses
        - Rewarding the miners
        - Updating the scores
        """
        # TODO(developer): Rewrite this function based on your protocol definition.
        return await forward(self)


# The main function parses the configuration and runs the validator.
if __name__ == "__main__":
    with Validator() as validator:
        while True:
            bt.logging.info("Validator running...", time.time())
            time.sleep(5)
