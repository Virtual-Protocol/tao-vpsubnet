# This is a sample miner that simply returns input * 2

import time
import typing
import bittensor as bt

# Bittensor Miner Template:
import template

# import base miner class which takes care of most of the boilerplate
from template.base.miner import BaseMinerNeuron

# Inference usage
from inference import inference
from protocol import ATASynapse
import base64
import uuid
import os

class EDGEMiner(BaseMinerNeuron):

    def __init__(self, config=None):
        super(EDGEMiner, self).__init__(config=config)

    def decode_and_save_wav(self, audio_input, output_path):
        # Decode base64 audio input
        decoded_audio = base64.b64decode(audio_input)
        
        # Write the decoded audio to a .wav file
        with open(output_path, "wb") as wav_file:
            wav_file.write(decoded_audio)
 

    async def forward(
        self, synapse: ATASynapse
    ) -> ATASynapse:
        """
        Processes the incoming 'ATASynapse' synapse by inferencing animation data from audio input.

        Args:
            synapse: The synapse object containing the 'audio_input' data.

        Returns:
            The synapse object with the 'animation_output' using bvh file format
        """
        
        # Convert the audio input into wav file
        root_dir = os.path.dirname(os.path.abspath(__file__))
        uid = str(uuid.uuid4())
        file_path = f"{root_dir}/{uid}.wav"
        self.decode_and_save_wav(synapse.audio_input, file_path)
        res = inference(file_path)
        synapse.animation_output = res
        return synapse

    async def blacklist(
        self, synapse: ATASynapse
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

        bt.logging.trace(
            f"Not Blacklisting recognized hotkey {synapse.dendrite.hotkey}"
        )
        return False, "Hotkey recognized!"

    async def priority(self, synapse: ATASynapse) -> float:
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
    
    def save_state(self):
        # TODO: Check what does this do
        pass

    def load_state(self):
        # TODO: Check what does this do
        pass


# This is the main function, which runs the miner.
if __name__ == "__main__":
    with EDGEMiner() as miner:
        while True:
            bt.logging.info("EDGE Miner running...", time.time())
            time.sleep(5)
