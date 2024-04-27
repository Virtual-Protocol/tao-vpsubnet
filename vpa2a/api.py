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

from flask import Flask, jsonify, request
from vpa2a.inference import inference
from vpa2a import postprocess
import os
import uuid
import bittensor as bt
import threading

app = Flask(__name__)

def try_remove_file(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        pass

def remove_files(files):
    for file in files:
        try_remove_file(file)

@app.route('/', methods=['POST'])
def handle_inference():
    data = request.get_json()
    
    if data is None:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    file_path = data.get('input')
    
    if file_path is None:
        return jsonify({'error': 'No input provided'}), 400
    
    root_dir = os.path.dirname(os.path.abspath(__file__)) + "/../vpa2a"
    uid = str(uuid.uuid4())
    
    pkl_file = inference(file_path)
    bvh_path = f"{root_dir}/data/outputs/{uid}.bvh"
    bt.logging.info(f"Post-processing {pkl_file}")
    fixed_pkl_file = postprocess.postprocess_pkl(pkl_file)
    postprocess.pkl2bvh(fixed_pkl_file, bvh_path)
    output = None
    with open(bvh_path, 'r') as file:
        output = file.read()

    #try_remove_file(file_path)
    output_audio_file = f"{root_dir}/data/outputs/output_{os.path.basename(file_path)}"
    thread = threading.Thread(target=remove_files, args=[[output_audio_file,pkl_file,fixed_pkl_file,bvh_path]])
    thread.start()

    response = {"output": output}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, port=5000)