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

import torch
from typing import List
from .rmse import compute_rmse

def sigmoid(x, temperature, shift):
    """
    Apply a sigmoid function to normalize scores.
    """
    return 1 / (1 + torch.exp(-temperature * (x - shift)))


def reward(query, response, response_time, max_response_time) -> float:
    """
    Reward the miner response to the dummy request. This method returns a reward
    value for the miner, which is used to update the miner's score.

    Returns:
    - float: The reward value for the miner.

    Inputs are both in .bvh file formats. 

    RMSE range of 0 - 4000. If MSE is 0 then returns 1 (most correct), if MSE is 4000 or above then returns 0.01
    """

    if response is None or len(response) == 0:
        return 0.0

    rmse = compute_rmse(response, query)

    min_score = 0.1
    max_score = 1.0
    max_allowable_rmse = 4000.0
    correctness_weight = 0.7
    speed_weight = 0.3

    if rmse > max_allowable_rmse:
        correctness_score = min_score
    else:
        # map a linear relationship between the max and min values of allowable RMSE to scores.
        k = (max_score - min_score) / max_allowable_rmse
        correctness_score = 1 - (rmse * k)

    normalized_speed_score = 1 - response_time / max_response_time
    
    # Apply sigmoid to speed score for normalization between 0 and 1
    speed_score = sigmoid(torch.tensor([normalized_speed_score]), temperature=1.0, shift=0.5).item()
    
    combined_score = (correctness_weight * correctness_score) + (speed_weight * speed_score)

    return combined_score


def get_rewards(
    self,
    query,
    responses,
) -> torch.FloatTensor:
    """
    Returns a tensor of rewards for the given query and responses.

    Args:
    - query (int): The query sent to the miner.
    - responses (List[str, float]): A list of responses from the miner.

    Returns:
    - torch.FloatTensor: A tensor of rewards for the given query and responses.
    """
    # dealing with empty response_times. 
    default_high_process_time = 120 
    max_response_time = 180

    for response in responses :
        if response[1] is None :
            response[1] = default_high_process_time

    # Get all the reward results by iteratively calling your reward() function.
    return torch.FloatTensor(
        [reward(query, response[0], response[1], max_response_time) for response in responses]
    ).to(self.device)
