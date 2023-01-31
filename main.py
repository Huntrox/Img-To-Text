import io
import base64
import os
import sys
from flask import Flask, request
from PIL import Image
import pytesseract
import cv2
import numpy


app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = './upload'
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


@app.route("/extract_text", methods=["POST"])
def extract_text_b64():
    
    image_b64 = request.json.get("image")
    image_bytes = base64.b64decode(image_b64)
    image = Image.open(io.BytesIO(image_bytes))
    
    text = extract_text(image)
    return text


@app.route("/extract_text_img", methods=["POST"])
def extrac_text_img_file():

    if 'img' not in request.files:
        return "No file"
    f = request.files['img']

    image = Image.open(f)
    text = extract_text(image)
    return text




def extract_text(img):
    
    gray_scaled = cv2.cvtColor(numpy.array(img), cv2.COLOR_BGR2GRAY)
    gray_scaled = cv2.threshold(gray_scaled, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #gray_scaled = cv2.medianBlur(gray_scaled, 1)
    
    filename = os.path.join(app.config['UPLOAD_FOLDER'],"{}.png".format(os.getpid()))
    cv2.imwrite(filename, gray_scaled)
    img = cv2.imread(filename)      
    

    if sys.platform.startswith('win'):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    
    text = pytesseract.image_to_string(img)
    os.remove(filename)
    return text


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)





