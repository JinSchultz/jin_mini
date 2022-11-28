import json
import base64
from flask import Response
import os

def make_succ_empty_response():
    data = json.dumps({'code': 0, 'data': {}})
    return Response(data, mimetype='application/json')


def make_succ_response(data):
    data = json.dumps({'code': 0, 'data': data})
    return Response(data, mimetype='application/json')


def make_err_response(err_msg):
    data = json.dumps({'code': -1, 'errorMsg': err_msg})
    return Response(data, mimetype='application/json')

def make_img_response(img_local_path):
    img_stream = ''
    img_f = open(img_local_path, 'rb')
    img_stream = img_f.read()
    img_stream = base64.b64encode(img_stream)
    img_f.close()
    os.remove(img_local_path)
    return img_stream