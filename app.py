from flask import Flask,render_template,request,flash, url_for, redirect
import os
from werkzeug.utils import secure_filename
import cv2
from PIL import Image
from rembg import remove

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'the random string'

def process(filename,oper):
    img = cv2.imread(f"upload/{filename}")
    match oper:
        case "greyh":
            new_img = cv2.imread(f"upload/{filename}",0)
            cv2.imwrite(f"static/{filename}",new_img)
            return filename
        case "pngh":
            new_img = cv2.imread(f"upload/{filename}")
            new_file = (f"{filename}.").split('.')[0]+".png"
            cv2.imwrite(f"static/{new_file}",new_img)
            return new_file
        case "jpegh":
            new_img = cv2.imread(f"upload/{filename}")
            new_file = (f"{filename}.").split('.')[0]+".jpeg"
            cv2.imwrite(f"static/{new_file}",new_img)
            return new_file
        case "webph":
            new_img = cv2.imread(f"upload/{filename}")
            new_file = (f"{filename}.").split('.')[0]+".webp"
            cv2.imwrite(f"static/{new_file}",new_img)
            return new_file
        case "pdfh":
            new_img = Image.open(f"upload/{filename}")
            new_file = new_img.convert('RGB')
            new_file.save(f"static/{(f"{filename}.").split('.')[0]+".pdf"}")
            img_temp = (f"{filename}.").split('.')[0]+".pdf"
            return img_temp
        case "remh":
            new_img = Image.open(f"upload/{filename}")
            new_file = remove(new_img)
            new_file.save(f"static/{(f"{filename}.").split('.')[0]+".png"}")
            img_temp = (f"{filename}.").split('.')[0]+".png"
            return img_temp



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/FeaturePage')
def feature():
    return render_template("feature.html")

@app.route('/edit',methods=["POST","GET"])
def edit():
    if request.method=="POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Not a Valid Request"
        file = request.files['file']
        oper = request.form.get('operation')
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "File not selected"
        if allowed_file(file.filename) == False:
            return "Not a Valid File"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(f"file name is {filename} and operation is {oper}")
            new_file = process(filename,oper)
            return redirect(f"static/{new_file}")
    return render_template("index.html")
    

if __name__ == '__main__':
    app.run(debug=True, port=5002)