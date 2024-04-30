from flask import Flask, jsonify, request, send_file
import uuid
import os
from inference import inference
from postprocess import postprocess_pkl, pkl2bvh
import sys
sys.path.append("./EDGE")
sys.path.append("./EDGE/dataset")
sys.path.append("./smpl2bvh")


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        status="ok",
    )


@app.route("/inference", methods=["POST"])
def inference_audio():
    # Extract the audio from the request
    audio = request.files.get("audio")

    if (audio is None) or (audio.filename == ""):
        return jsonify(
            status="error",
            message="Missing audio file")

    # check file extension is .wav
    if audio.filename.split(".")[-1] != "wav":
        return jsonify(
            status="error",
            message="Invalid file extension")

    uid = uuid.uuid4()
    file_path = f"./data/inputs/{uid}.wav"
    audio.save(file_path)
    
    # Run the inference
    pkl_file = inference(file_path)

    bvh_path = f"./data/outputs/{uid}.bvh"

    fixed_pkl_file = postprocess_pkl(pkl_file)
    pkl2bvh(fixed_pkl_file, bvh_path)

    # delete the file based on filename
    os.remove(file_path)
    os.remove(fixed_pkl_file)
    os.remove(pkl_file)

    return send_file(bvh_path, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
