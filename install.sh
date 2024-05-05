#!/bin/bash

cd vpa2a
echo "Creating runtime directories"
mkdir -p data/inputs
mkdir -p data/outputs

echo "Cloning EDGE repository"
git clone https://github.com/Stanford-TML/EDGE.git

echo "Downloading pre-trained model weights"
cd EDGE
touch __init__.py
pip install gdown
gdown https://drive.google.com/uc?id=1BAR712cVEqB8GR37fcEihRV_xOC-fZrZ

echo "Installing Conda packages"
conda install -y pytorch=1.13.1 torchvision pytorch-cuda=11.6 -c pytorch -c nvidia
conda install -y -c fvcore -c iopath -c conda-forge fvcore iopath
conda install -y pytorch3d -c pytorch3d

echo "Installing postprocessor"
git clone https://github.com/KosukeFukazawa/smpl2bvh.git

cd ../../
echo "Installing Python packages"
pip install -r requirements.txt
pip install -r vpa2a/requirements.txt