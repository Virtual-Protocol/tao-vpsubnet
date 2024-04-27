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

import time
import typing
import bittensor as bt
import requests

# import base miner class which takes care of most of the boilerplate
from vpa2a.base.miner import BaseMinerNeuron

# Inference usage
from vpa2a.inference import inference
from vpa2a import postprocess
from vpa2a.protocol import VPA2ASynapse
import base64
import uuid
import os

class VPA2AMiner(BaseMinerNeuron):

    def __init__(self, config=None):
        super(VPA2AMiner, self).__init__(config=config)

    def decode_and_save_wav(self, audio_input, output_path):
        # Decode base64 audio input
        decoded_audio = base64.b64decode(audio_input)
        
        # Write the decoded audio to a .wav file
        with open(output_path, "wb") as wav_file:
            wav_file.write(decoded_audio)

    def download_and_save_wav(self, url, file_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)

    async def forward(
        self, synapse: VPA2ASynapse
    ) -> VPA2ASynapse:
        """
        Processes the incoming 'VPA2ASynapse' synapse by inferencing animation data from audio input.

        Args:
            synapse: The synapse object containing the 'audio_input' data.

        Returns:
            The synapse object with the 'animation_output' using bvh file format
        """

        root_dir = os.path.dirname(os.path.abspath(__file__)) + "/../vpa2a"
        uid = str(uuid.uuid4())
        file_path = f"{root_dir}/data/inputs/{uid}.wav"
        if synapse.is_url():
            self.download_and_save_wav(synapse.audio_input, file_path)
        else:
            self.decode_and_save_wav(synapse.audio_input, file_path)
        
        bt.logging.info(f"Inferencing {file_path}")
        pkl_file = inference(file_path)
        bvh_path = f"{root_dir}/data/outputs/{uid}.bvh"
        bt.logging.info(f"Post-processing {pkl_file}")
        fixed_pkl_file = postprocess.postprocess_pkl(pkl_file)
        postprocess.pkl2bvh(fixed_pkl_file, bvh_path)
        with open(bvh_path, 'r') as file:
            synapse.animation_output = file.read()

        # cleanup
        os.remove(file_path)
        os.remove(pkl_file)
        os.remove(fixed_pkl_file)
        os.remove(bvh_path)

        return synapse

    async def blacklist(
        self, synapse: VPA2ASynapse
    ) -> typing.Tuple[bool, str]:
        # TODO(developer): Define how miners should blacklist requests.
        uid = self.metagraph.hotkeys.index(synapse.dendrite.hotkey)
        if (
            not self.config.blacklist.allow_non_registered
            and synapse.dendrite.hotkey not in self.metagraph.hotkeys
        ):
            # Ignore requests from un-registered entities.
            bt.logging.trace(
                f"Blacklisting un-registered hotkey {synapse.dendrite.hotkey}"
            )
            return True, "Unrecognized hotkey"

        if self.config.blacklist.force_validator_permit:
            # If the config is set to force validator permit, then we should only allow requests from validators.
            if not self.metagraph.validator_permit[uid]:
                bt.logging.warning(
                    f"Blacklisting a request from non-validator hotkey {synapse.dendrite.hotkey}"
                )
                return True, "Non-validator hotkey"

        # Get the caller stake
        caller_uid = self.metagraph.hotkeys.index(
            synapse.dendrite.hotkey
        )  # Get the caller index.
        caller_stake = float(
            self.metagraph.S[caller_uid]
        )  # Return the stake as the priority.
        if caller_stake < 100: #TODO: Change this to a more reasonable value
            bt.logging.trace(
                f"Blacklisting hotkey {synapse.dendrite.hotkey}, not enough stake"
            )
            return True, "Not enough stake"

        bt.logging.trace(
            f"Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}"
        )
        return False, "Hotkey recognized!"

    async def priority(self, synapse: VPA2ASynapse) -> float:
        # TODO(developer): Define how miners should prioritize requests.
        caller_uid = self.metagraph.hotkeys.index(
            synapse.dendrite.hotkey
        )  # Get the caller index.
        prirority = float(
            self.metagraph.S[caller_uid]
        )  # Return the stake as the priority.
        bt.logging.trace(
            f"Prioritizing {synapse.dendrite.hotkey} with value: ", prirority
        )
        return prirority


# This is the main function, which runs the miner.
if __name__ == "__main__":
    with VPA2AMiner() as miner:
        while True:
            bt.logging.info("VPA2AMiner Miner running...", time.time())
            time.sleep(5)
