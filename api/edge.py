# The MIT License (MIT)
# Copyright © 2021 Yuma Rao
# Copyright © 2023 Opentensor Foundation
# Copyright © 2023 Opentensor Technologies Inc

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
from typing import List, Optional, Union, Any, Dict
from neurons.protocol import ATASynapse
from bittensor.subnets import SubnetsAPI
import base64

class EDGEAPI(SubnetsAPI):
    def __init__(self, wallet: "bt.wallet"):
        super().__init__(wallet)
        self.netuid = 1
        self.name = "ata"


    def prepare_synapse(self, input: str) -> ATASynapse:
        synapse = ATASynapse()
        synapse.audio_input = input
        
        return synapse

    def process_responses(
        self, responses: List[Union["bt.Synapse", Any]]
    ) -> List[int]:
        outputs = []
        for response in responses:
            if response.dendrite.status_code != 200:
                continue
            outputs.append(response.animation_output)
        return outputs
    
    def deserialize(self) -> int:
        return self.animation_output
