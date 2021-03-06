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


def meal(param):
    rawMeal = ''
    jsonMeal = ''
    meal = ''

    if (param["day"] == "오늘"):
        rawMeal = json.loads(
            getData('http://dsm2015.cafe24.com/meal/' + datetime.date.isoformat(datetime.date.today())))
    elif (param["day"] == "내일"):
        rawMeal = json.loads(getData('http://dsm2015.cafe24.com/meal/' + datetime.date.isoformat(
            datetime.date.today() + datetime.timedelta(days=1))))

    if (param["meal"] == "아침 급식"):
        jsonMeal = rawMeal["breakfast"]
    elif (param["meal"] == "점심 급식"):
        jsonMeal = rawMeal["lunch"]
    elif (param["meal"] == "저녁 급식"):
        jsonMeal = rawMeal["dinner"]

    for i in jsonMeal:
        if (meal == "혼합"):
            continue
        meal += i + ', '

    meal = meal[0:-2]  # 여기까지 급식 받아오기

    mealTxt = param["day"] + "의 " + param["meal"] + "은 " + meal + "입니다."
    textreq = {
        "fulfillmentText": mealTxt,
        "payload":
            {"google":
                 {"expectUserResponse": False, "richResponse":
                     {"items":
                         [
                             {"simpleResponse":
                                  {"textToSpeech": mealTxt}
                              }
                         ]
                     }
                  }
             }
    }

    return textreq


@app.route('/')
def hello():
    return 'I am DMS Assistant!'


@app.route('/meal')
def rawMeal():
    meal = getData('http://dsm2015.cafe24.com/meal/' + datetime.date.isoformat(datetime.date.today()))
    response = Response(meal)
    response.headers["Content-Type"] = 'application/json; charset=utf8'
    return response


@app.route('/google', methods=['POST'])
def google():
    req = request.json
    intent = req["queryResult"]["intent"]["displayName"]
    queryText = req["queryResult"]["queryText"]
    param = req["queryResult"]["parameters"]
    rawResponse = ''

    if (intent == "askMeal"):
        rawResponse = json.dumps(meal(param), ensure_ascii=False)

    response = Response(rawResponse)
    response.headers["Content-Type"] = 'application/json; charset=utf8'
    return response


if __name__ == '__main__':
    app.run()
