import io
import cv2
import uuid
import os 
import cloudinary
import cloudinary.uploader
import firebase_admin
import numpy as np
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for
from firebase_admin import credentials, firestore
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Cloudinary Config
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
    secure=True
)

app = Flask(__name__)

allowed_extensions = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions

def make_sketch(img):
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(grayed)
    blurred = cv2.GaussianBlur(inverted, (5, 5), sigmaX=0, sigmaY=0)
    final_result = cv2.divide(grayed, 255 - blurred, scale=220)
    return final_result

def upload_to_cloudinary(image_np, filename):
    # Convert NumPy image to bytes buffer
    _, buffer = cv2.imencode('.jpg', image_np)
    byte_stream = io.BytesIO(buffer)

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(byte_stream, folder="sketches", public_id=filename, resource_type="image")
    return upload_result['secure_url']

@app.route('/')
def home():
    org_url = request.args.get('org')
    sketch_url = request.args.get('sketch')
    return render_template('home.html', org_img_url=org_url, sketch_img_url=sketch_url)

@app.route('/sketch', methods=['POST'])
def sketch():
    file = request.files['file']
    if file and allowed_file(file.filename):
        img_bytes = file.read()

        # Convert to OpenCV image
        np_img = np.array(Image.open(io.BytesIO(img_bytes)).convert('RGB'))
        cv_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2BGR)

        # Create sketch
        sketch_img = make_sketch(cv_img)

        # Unique names
        unique_id = str(uuid.uuid4())
        original_filename = f"{unique_id}_original"
        sketch_filename = f"{unique_id}_sketch"

        # Upload to Cloudinary
        original_url = upload_to_cloudinary(cv_img, original_filename)
        sketch_url = upload_to_cloudinary(sketch_img, sketch_filename)

        return redirect(url_for('home', org=original_url, sketch=sketch_url))
    return "Invalid file", 400

@app.route('/gallery')
def gallery():
    result = cloudinary.Search()\
        .expression("public_id:sketches/*")\
        .sort_by("created_at", "desc")\
        .max_results(30)\
        .execute()

    print(len(result))
    images = result.get("resources", [])
    print(len(images))
    sketch_data = [{
        'url': img['secure_url'],
        'created_at': img['created_at'],
        'public_id': img['public_id']
    } for img in images]

    for img in images:
        print(sketch_data)
    return render_template("gallery.html", sketches=sketch_data)

if __name__ == '__main__':
    app.run(debug=True)
