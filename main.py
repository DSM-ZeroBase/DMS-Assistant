from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'I am DMS Assistant!'

@app.route('/meal')
def getmeal():
    return 'meal'

if __name__ == '__main__':
    app.run()
