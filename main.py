from flask import Flask, Response, request
import requests
import datetime

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
    lastReq = ''
    if request.method == 'POST':
        lastReq = request.form
        return
    else:
        return lastReq


if __name__ == '__main__':
    app.run()
