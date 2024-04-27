# The MIT License (MIT)
# Copyright © 2024 VirtualProtocol

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

import bittensor as bt

from vpa2a.protocol import VPA2ASynapse
from .reward import get_rewards
from vpa2a.base.utils.uids import get_random_uids
import os
import requests

def get_animation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        bt.logging.error(f"Failed to retrieve animation data from API: {response.status_code}")
        return None

def get_challenge():
    url = os.getenv("VALIDATOR_LIB")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        animation = get_animation(data["animation"])
        if not animation:
            return None, None
        return data["audio"], animation
    else:
        bt.logging.error(f"Failed to retrieve challenge from API: {response.status_code}")
        return None, None

async def forward(self):
    print("forwarding")
    audio_input, animation_output = get_challenge()
    if not audio_input:
        return
    miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)
    synapse = VPA2ASynapse(audio_input=audio_input)

    # The dendrite client queries the network.
    responses = await self.dendrite(
        # Send the query to selected miner axons in the network.
        axons=[self.metagraph.axons[uid] for uid in miner_uids],
        # Construct a dummy query. This simply contains a single integer.
        synapse=synapse,
        # All responses have the deserialize function called on them before returning.
        # You are encouraged to define your own deserialization function.
        deserialize=True,
    )
    print("Returned")
    print(responses)
    # Log the results for monitoring purposes.
    bt.logging.info(f"Received responses: {responses}")

    rewards = get_rewards(self, query=animation_output, responses=responses)

    bt.logging.info(f"Scored responses: {rewards}")
    # Update the scores based on the rewards. You may want to define your own update_scores function for custom behavior.
    self.update_scores(rewards, miner_uids)
