# EDGE Model Reference Documentation

This provides updated documentation to setup the development and inference environment for the [EDGE](https://github.com/Stanford-TML/EDGE/tree/main) model as reference.

## Installation and Environment Setup
Clone the EDGE repository.
```bash
git clone https://github.com/Stanford-TML/EDGE.git
```

Install the required dependencies. We highly recommend using a conda environment for this especially for pytorch3d.
```bash
conda create -n pytorch3d python=3.9
conda activate pytorch3d
conda install pytorch=1.13.0 torchvision pytorch-cuda=11.6 -c pytorch -c nvidia
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
pip install scikit-image matplotlib imageio plotly opencv-python
conda install pytorch3d -c pytorch3d

apt-get install libsndfile1 # (might be needed for the jukemirlib library)
pip install git+https://github.com/rodrigo-castellon/jukemirlib.git

pip install wandb einops p-tqdm
```

Download the pretrained model weights from the provided link.
```bash
pip install gdown
gdown https://drive.google.com/uc?id=1BAR712cVEqB8GR37fcEihRV_xOC-fZrZ
```

## Inference
In the root of the EDGE directory, generate animation by providing an audio input in the form a .wav file. Copy our provided inference file adapted from test.py from EDGE over to the root of the EDGE directory for more automatic use to generate animation length of entire wav file. The test.py provided by EDGE samples a random snippet of output length specified.
```bash
python inference.py --music_dir "{output_folder}"/ --save_motions --motion_save_dir "{motion_folder}" --out_length -1
```

You can find visualization of the animation in renders directory and the generated animation in smpl format as a .pkl file in the output directory.

## Post-processing
The animation generated from the EDGE model is in the SMPL format. This Subnet requires the animation to be in the BVH format. We provide a script to convert the SMPL format to BVH format. We also provide a script to first fix the formatting of the output SMPL file before converting it to BVH format.

First, install the required libraries for conversion and post-processing.

```bash
pip install git+https://github.com/mattloper/chumpy
pip install smplx[all]
```

Fix the output SMPL file.
```bash
python fix_edge_smpl.py --file_path edge_smpl_out.pkl
```

Convert the fixed SMPL file to bvh using the [smpl2bvh](https://github.com/KosukeFukazawa/smpl2bvh.git) repository. To convert an SMPL file, please download the SMPL body files (MALE, FEMALE, NEUTRAL) from https://smpl.is.tue.mpg.de/index.html and place them in the data directory - requires you to register for an account.
```bash
cd smpl2bvh
git clone https://github.com/KosukeFukazawa/smpl2bvh.git
python smpl2bvh.py --gender MALE --poses fix_edge_smpl_out.pkl —-fps 30 --output output.bvh --mirror
```

## Encountered issues
1. Make sure ffmpeg with libx264 is installed properly for rendering of stickman. Follow instructions in this [issue](https://gist.github.com/Wilann/a187a3aebc19914605bc6a7bd90b7986) to install appropriately.


