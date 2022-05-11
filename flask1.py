
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

@app.route('/' ,methods=['GET'])
def hello():
    return render_template('upload.html')

@app.route('/upload' ,methods=['GET'])
def upload_file():
    return render_template('upload.html')

@app.route('/uploader' ,methods=['POST'])
def uploader():
    data = request.data
    url = 'http://recognition:5678/recog'
    # url = 'http://localhost:5678/recog'

    myobj = data
    from PIL import Image
    from io import BytesIO
    img = Image.open(BytesIO(myobj)).convert('RGB')
    w, h = img.size
    img = img.resize((int(w * 0.5), int(h * 0.5)), Image.ANTIALIAS)
    compressed_bytes = BytesIO()
    img.save(compressed_bytes, format='jpeg')

    # nimg = Image.open(BytesIO(compressed_bytes.getvalue()))
    # print(compressed_bytes.tell())
    # nimg.show()
    x = requests.post(url, data=compressed_bytes.getvalue())

    result_json = json.loads(x.text)
    result = result_json['result']
    print(result)

    import time

    import base64
    base64_str = base64.b64encode(compressed_bytes.getvalue()).decode("ascii")
    base64_str = 'data:image/jpeg;base64,' + base64_str

    ## payload = str({"result": result, "object": str(myobj)})
    # print(base64_str)
    payload = str("result={};object={}".format(result, base64_str))
    r.set(int(time.time()), payload)

    return x.text

@app.route('/get_display_image', methods=['GET'])
def get_display_image():
    img_keys = r.keys()
    img_keys.sort(reverse=True)
    img_keys = img_keys[:9]
    img_list = {}
    i = 0
    for elem in img_keys:
        tmp = (r.get(elem)).decode('utf-8')

        label = tmp.split("=")[1].split(";")[0]
        data = tmp.split("object=")[1]

        payload = {"label": label, "data": data}
        img_list[i] = payload

        i += 1

        # print(img_list)
    return img_list

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 5100)
