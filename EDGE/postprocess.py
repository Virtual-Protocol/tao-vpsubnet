import os
import pickle
import argparse
import numpy as np


def main(args):

    motion_file = args.file_path
    motion_data = pickle.load(open(motion_file, "rb"))
    trans = motion_data["smpl_trans"]
    pose = motion_data["smpl_poses"]

    # fix smpl file by adding scale                                                                                                                                                                       
    scale = np.array([1.0])

    # Get the input file name without the extension                                                                                                                                                       
    input_filename = os.path.splitext(os.path.basename(motion_file))[0]
    output_filename = f"{input_filename}_fixed_smpl.pkl"
    out_data = {"smpl_trans": trans, "smpl_poses": pose, "smpl_scaling": scale}
    pickle.dump(out_data, open(output_filename, "wb"))

    print(f"Fixed smpl saved as: {output_filename}")

    # test fixed smpl                                                                                                                                                                                     
    new_smpl = pickle.load(open(output_filename, "rb"))
    print("trans: ", new_smpl["smpl_trans"].shape)
    print("poses: ", new_smpl["smpl_poses"].shape)
    print("scale: ", new_smpl["smpl_scaling"])



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", type=str)
    args = parser.parse_args()
    main(args)

