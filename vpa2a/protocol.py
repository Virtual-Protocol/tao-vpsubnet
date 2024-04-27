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
import typing

class VPA2ASynapse(bt.Synapse):
    """
    This protocol helps in handling request and response communication between
    the miner and the validator.

    Attributes:
    - audio_input: Base64 encoded audio input
    - animation_output: The animation output
    - input_type: Type indicator: 'data' for base64 encoded audio, 'url' for audio URL
    """

    input_type: str = 'url'

    # Required request input, filled by sending dendrite caller.
    audio_input: str = ""

    # Optional request output, filled by receiving axon.
    animation_output: typing.Optional[str] = ""

    def deserialize(self) -> str:
        return self.animation_output
    
    def is_url(self) -> bool:
        """ Check if the input is a URL. """
        return self.input_type == 'url'
