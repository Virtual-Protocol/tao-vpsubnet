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

import os
import pickle
import numpy as np
import sys
sys.path.append("./smpl2bvh")
from smpl2bvh import smpl2bvh
import bittensor as bt

def pkl2bvh(input, output):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = f"{root_dir}/smpl2bvh/data/smpl/"
    smpl2bvh(model_path=model_path, poses=input, mirror=False, fps=30, output=output)
    bt.logging.info(f"Bvh saved to {output}")

def postprocess_pkl(motion_file):
    motion_data = pickle.load(open(motion_file, "rb"))
    trans = motion_data["smpl_trans"]
    pose = motion_data["smpl_poses"]

    # fix smpl file by adding scale                                                                                                                                                                       
    scale = np.array([1.0])

    # Get the input file name without the extension                                                                                                                                                       
    input_filename = os.path.splitext(os.path.basename(motion_file))[0]
    root_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = f"{root_dir}/data/outputs/fixed_{input_filename}.pkl"
    out_data = {"smpl_trans": trans, "smpl_poses": pose, "smpl_scaling": scale}
    pickle.dump(out_data, open(output_filename, "wb"))

    bt.logging.info(f"Fixed smpl saved as: {output_filename}")

    return output_filename
