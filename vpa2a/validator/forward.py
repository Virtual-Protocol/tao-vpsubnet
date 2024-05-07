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
from tempfile import TemporaryDirectory

def get_animation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        bt.logging.error(f"Failed to retrieve animation data from API: {response.status_code}")
        return None


def get_challenge(tempdir):
    url = os.getenv("VALIDATOR_LIB")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        animation = get_animation(data["animation"])
        animation_path = os.path.join(tempdir, "animation.bvh")
        if animation:
            with open(animation_path, "w") as f:
                f.write(animation)
        return data["audio"], animation_path
    else:
        bt.logging.error(f"Failed to retrieve challenge from API: {response.status_code}")
        return None, None


async def forward(self):
    miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)
    temp_dir = TemporaryDirectory()
    try:
        audio_input, animation_output = get_challenge(temp_dir.name)
        
        if audio_input is None:
            raise Exception("Failed to retrieve challenge data")
        
        synapse = VPA2ASynapse(audio_input=audio_input)

        # The dendrite client queries the network.
        responses = await self.dendrite(
            axons=[self.metagraph.axons[uid] for uid in miner_uids],
            synapse=synapse,
            timeout=180,
            deserialize=False,
        )
        # Write responses to disk
        response_paths = []
        for idx, response in enumerate(responses):
            rpath = ""
            if len(response.animation_output) > 0:
                rpath = f"{temp_dir.name}/r{idx}.bvh"
                with open(os.path.join(temp_dir.name, rpath), "w") as f:
                    f.write(response.animation_output)
            response_paths.append([rpath, response.dendrite.process_time])

        bt.logging.info(f"Rewarding with query {animation_output} and responses {response_paths}")
        
        rewards = get_rewards(
            self, query=animation_output, responses=response_paths)
        bt.logging.info(f"Scored responses: {rewards}")
        # Update the scores based on the rewards. You may want to define your own update_scores function for custom behavior.
        self.update_scores(rewards, miner_uids)
    except Exception as e:
        bt.logging.error(f"Failed to forward query with exception: {e}")
    finally:
        temp_dir.cleanup()



