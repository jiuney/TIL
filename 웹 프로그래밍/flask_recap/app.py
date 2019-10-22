from flask import Flask
from flask import render_template
from flask import request
import random
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/mulcam')
def mulcam():
    return "We are at Mulcam!"

@app.route('/greeting/<string:name>')
def greeting(name):
    return f'반갑습니다. {name}님!'

@app.route('/cube/<int:num>')
def cube(num):
    result = num**3
    return str(result)

@app.route('/dinner/<int:person>')
def dinner(person):
    menu = ['뼈해장국', '짬뽕', '초밥', '샐러드']
    order = random.sample(menu, person)
    return str(order)

@app.route('/html')
def html():
    markup = """
    <h1>This is h1 tag.</h1>
    <p>This is p tag.</p>
    """
    return markup

@app.route("/html_file")
def html_file():
    return render_template('html_file.html')

@app.route('/hi/<string:name>')
def hi(name):
    return render_template('hi.html', your_name=name)

@app.route('/naver')
def naver():
    return render_template('naver.html')

@app.route('/send')
def send():
    return render_template('send.html')

@app.route('/receive')
def receive():
    name = request.args.get("name")
    message = request.args.get("message")
    return render_template('receive.html', name=name, message=message)

@app.route('/vonvon')
def vonvon():
    return render_template('vonvon.html')

@app.route('/result')
def result():
    name = request.args.get("name")
    features = ['돈복', '순수함', '사랑스러움', '일복', '명예']
    chosen = random.sample(features, 3)
    return render_template('result.html', name=name, chosen=chosen)

if __name__ == "__main__":
    app.run(debug=True)
