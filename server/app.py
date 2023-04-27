from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from utils import get_captions, empty_temp_folder
from flask_cors import CORS, cross_origin
from flask import Flask, request
import keras_ocr
import base64
import torch
import os

# Models Setup
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
pipeline=keras_ocr.pipeline.Pipeline()
model.to(device)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def start():
    return "server started"

@app.route("/generate_captions", methods = ['POST'])
@cross_origin()
def generate_captions():    
    body = request.json
    images = body["images"]
    empty_temp_folder()
    for i, img in enumerate(images):
        decoded_data = base64.b64decode(img["base64_file"].split("base64,")[1])
        img_file = open("temp/" + str(i) + 'image.jpeg', 'wb')
        img_file.write(decoded_data)
        img_file.close()
    return get_captions(body, model, feature_extractor, tokenizer, device, pipeline)

if __name__ == "__main__":
    app.run(debug=True)