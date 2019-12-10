# coding:utf-8
import json
import cpca
import synonyms

from flask import Flask, request

app = Flask(__name__)

MY_URL = '/address/'


# get
@app.route(MY_URL + 'format', methods=['GET'])
def format_address():
    param = request.args.to_dict()
    addr = param['address']

    if addr is not None:
        return cpca.parseAddr(addr)
    else:
        return {"err_msg":"address param empty"}

# post
@app.route(MY_URL + 'similarity', methods=['POST'])
def get_similarity():
    param = request.form
    v1 = param['addr1']
    v2 = param['addr2']

    if v1!="" and v2!="":
        return {"similarity":synonyms.compare(v1, v2)}
    else:
        return {"err_msg":"address param empty"}

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=8000)
    app.run(debug=False)
