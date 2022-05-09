from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

@app.route('/')
def hello():
    return 'hello docker&flask'

@app.route('/upload',methods=['GET'])
def upload_file():
    return render_template('upload.html')

@app.route('/uploader',methods=['POST'])
def uploader():
    data = request.data
    url = 'http://recognition:5678/recog'

    myobj = data

    x = requests.post(url, data=myobj)
    print(x.text)
    return x.text

if __name__ == '__main__':
   app.run(debug=True, host = '0.0.0.0', port = 5100)