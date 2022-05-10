

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
import redis
import json

import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
app.static_folder = 'templates/static'

# r = redis.Redis(host='112.74.161.101', port=32003)
r = redis.Redis(host='redis', port=6379)

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
    # url = 'http://localhost:5678/recog'

    myobj = data

    x = requests.post(url, data=myobj)
    result_json = json.loads(x.text)
    result = result_json['result']
    print(result)

    import uuid
    uuid = uuid.uuid1()

    payload = str({"result": result, "object": myobj})
    r.set(int(uuid), payload)

    return x.text

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5100)
