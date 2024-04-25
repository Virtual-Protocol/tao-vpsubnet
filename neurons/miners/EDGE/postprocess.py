import os
import pickle
import argparse
import numpy as np
import sys
sys.path.append("./smpl2bvh")
from smpl2bvh import smpl2bvh

def pkl2bvh(input, output):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = f"{root_dir}/smpl2bvh/data/smpl/"
    smpl2bvh(model_path=model_path, poses=input, mirror=False, fps=30, output=output)
    print(f"Bvh saved to {output}")

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

    print(f"Fixed smpl saved as: {output_filename}")

    return output_filename
