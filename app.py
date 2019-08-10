import json
import os
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    data = ""
    with open(os.getcwd() + "/output.json") as f:
        data = json.loads(f.read())
    return render_template('template.html', data=get_page(1))


@app.route('/get_page/<int:page_number>')
def get_page(page_number):
    data = ""
    with open(os.getcwd() + "/output.json") as f:
        data = json.loads(f.read())
    page_data = data[10*(page_number-1):10*page_number]
    return render_template("cards.html", data=page_data)