import bittensor as bt


class ATASynapse(bt.Synapse):
    """
    This protocol helps in handling request and response communication between
    the miner and the validator.

    Attributes:
    - audio_input: Base64 encoded audio input
    - animation_output: The animation output
    """

    # Required request input, filled by sending dendrite caller.
    audio_input: str = ""

    # Optional request output, filled by receiving axon.
    animation_output: str = ""

    def deserialize(self) -> int:
        """
        Deserialize the dummy output. This method retrieves the response from
        the miner in the form of animation_output, deserializes it and returns it
        as the output of the dendrite.query() call.
        """
        return self.animation_output
