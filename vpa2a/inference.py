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

import glob
import os
from functools import cmp_to_key
from pathlib import Path
from tempfile import TemporaryDirectory
import random

import numpy as np
import torch
from tqdm import tqdm

from EDGE.data.slice import slice_audio
from EDGE.EDGE import EDGE
from EDGE.data.audio_extraction.baseline_features import extract as baseline_extract
from EDGE.data.audio_extraction.jukebox_features import extract as juke_extract

# sort filenames that look like songname_slice{number}.ext

def key_func(x): return int(os.path.splitext(
    x)[0].split("_")[-1].split("slice")[-1])


def stringintcmp_(a, b):
    aa, bb = "".join(a.split("_")[:-1]), "".join(b.split("_")[:-1])
    ka, kb = key_func(a), key_func(b)
    if aa < bb:
        return -1
    if aa > bb:
        return 1
    if ka < kb:
        return -1
    if ka > kb:
        return 1
    return 0


stringintkey = cmp_to_key(stringintcmp_)


def inference(wav_file):
    opt = type('DynamicObject', (object,), {
        "feature_type": "jukebox",
        "out_length": 30,
        "processed_data_dir":"data/dataset_backups/",
        "render_dir": "",
        "checkpoint": "checkpoint.pt",
        "save_motions": True,
        "cache_features": False,
        "no_render": True,
        "use_cached_features": False,
        "feature_cache_dir": "cached_features/",
        "motion_save_dir":""
    })
    root_dir = os.path.dirname(os.path.abspath(__file__))
    opt.motion_save_dir = f"{root_dir}/data/outputs"
    opt.render_dir = f"{root_dir}/data/outputs"
    opt.checkpoint = f"{root_dir}/EDGE/checkpoint.pt"
    opt.out_length = -1

    feature_func = juke_extract if opt.feature_type == "jukebox" else baseline_extract

    if opt.out_length > 0:
        sample_length = opt.out_length
        sample_size = int(sample_length / 2.5) - 1

    temp_dir_list = []
    all_cond = []
    all_filenames = []

    print("Computing features for input music")
    # create temp folder (or use the cache folder if specified)
    if opt.cache_features:
        songname = os.path.splitext(os.path.basename(wav_file))[0]
        save_dir = os.path.join(opt.feature_cache_dir, songname)
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        dirname = save_dir
    else:
        temp_dir = TemporaryDirectory()
        temp_dir_list.append(temp_dir)
        dirname = temp_dir.name
    # slice the audio file
    print(f"Slicing {wav_file}")
    slice_audio(wav_file, 2.5, 5.0, dirname)
    file_list = sorted(glob.glob(f"{dirname}/*.wav"), key=stringintkey)
    if opt.out_length > 0:
        # randomly sample a chunk of length at most sample_size
        rand_idx = random.randint(0, len(file_list) - sample_size)
    else:
        rand_idx = 0
        sample_size = len(file_list)
    cond_list = []
    # generate juke representations
    print(f"Computing features for {wav_file}")
    for idx, file in enumerate(tqdm(file_list)):
        # if not caching then only calculate for the interested range
        if (not opt.cache_features) and (not (rand_idx <= idx < rand_idx + sample_size)):
            continue
        # audio = jukemirlib.load_audio(file)
        # reps = jukemirlib.extract(
        #     audio, layers=[66], downsample_target_rate=30
        # )[66]
        reps, _ = feature_func(file)
        # save reps
        if opt.cache_features:
            featurename = os.path.splitext(file)[0] + ".npy"
            np.save(featurename, reps)
        # if in the random range, put it into the list of reps we want
        # to actually use for generation
        if rand_idx <= idx < rand_idx + sample_size:
            cond_list.append(reps)
    cond_list = torch.from_numpy(np.array(cond_list))
    all_cond.append(cond_list)
    all_filenames.append(file_list[rand_idx: rand_idx + sample_size])

    model = EDGE(opt.feature_type, opt.checkpoint)
    model.eval()

    # directory for optionally saving the dances for eval
    fk_out = None
    if opt.save_motions:
        fk_out = opt.motion_save_dir

    print("Generating dances")
    for i in range(len(all_cond)):
        data_tuple = None, all_cond[i], all_filenames[i]
        model.render_sample(
            data_tuple, "output", opt.render_dir, render_count=-1, fk_out=fk_out, render=not opt.no_render
        )

    torch.cuda.empty_cache()
    for temp_dir in temp_dir_list:
        temp_dir.cleanup()
    
    input_filename = os.path.splitext(os.path.basename(wav_file))[0]
    return f"{opt.render_dir}/output_{input_filename}.pkl"