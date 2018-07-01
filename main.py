from flask import Flask, Response, request
import requests
import datetime
import json

app = Flask(__name__)


def getData(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return 'error'


@app.route('/')
def hello():
    return 'I am DMS Assistant!'


@app.route('/meal')
def rawMeal():
    meal = getData('http://dsm2015.cafe24.com/meal/' + datetime.date.isoformat(datetime.date.today()))
    response = Response(meal)
    response.headers["Content-Type"] = 'application/json; charset=utf8'
    return response


@app.route('/google', methods=['POST', 'GET'])
def google():
    if request.method == 'POST':
        rawReq = request.form
        req = json.load(rawReq)
        return req
    else:
        return


if __name__ == '__main__':
    app.run()
