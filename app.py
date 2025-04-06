import cv2 
import os 
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, redirect, url_for 

upload_folder = 'C:/Users/vaish/OneDrive/Documents/Projects/Make_Sketches_From_Images/static/uploads' #save sketches here

allowed_extensions = set(['png', 'jpg', 'jpeg'])

# Defining our sketch making flask app
app = Flask(__name__)
app.config['SEND_FILE_MAX_aGE_DEFAULT'] = 0 # remove that file from the cache after its use
app.config['UPLOAD_FOLDER'] = upload_folder
app.secret_key = 'urawizardharry' # SET SECRET KEY IN .ENV

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions

def make_sketch(img):
    # Converts the image to grayscale. This simplifies the image by removing color info — we're working only with intensity now.
    grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Invert the grayscale image — black becomes white, white becomes black.
    inverted = cv2.bitwise_not(grayed)
    # Applies a Gaussian blur to the inverted image. If the kernel size (a, b) is pretty large — this softens details a lot.
    blurred = cv2.GaussianBlur(inverted, (5, 5), sigmaX=0, sigmaY=0)
    # 255 - blurred reinverts the blurred image. cv2.divide() then blends the original grayscale with this result in a way that highlights edges and lines, mimicking a pencil sketch.
    final_result = cv2.divide(grayed, 255 - blurred, scale=220)
    return final_result

@app.route('/')
def home():
    org_img = request.args.get('org_img_name')
    sketch_img = request.args.get('sketch_img_name')
    return render_template('home.html', org_img_name=org_img, sketch_img_name=sketch_img)

@app.route('/sketch', methods=['POST'])
def sketch():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = cv2.imread(upload_folder+'/'+filename)
        sketch_img = make_sketch(img)
        sketch_img_name = filename.split('.')[0]+"_sketch.jpg"
        _ = cv2.imwrite(upload_folder+'/'+sketch_img_name, sketch_img)
        return redirect(url_for('home', org_img_name=filename, sketch_img_name=sketch_img_name))
    
if __name__ == '__main__':
    app.run(debug=True)