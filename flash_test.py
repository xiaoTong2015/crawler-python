#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import json

app = Flask(__name__)
# 读取json文件
def load_json():
    with open('data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template("form.html")

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    # 需要从request对象读取表单内容：
    if username=='admin' and password=='password':
        return render_template("signin-ok.html",username=username)
    return render_template('form.html',message='Bad username or password', username=username)

@app.route('/show', methods=['GET'])
def showJson():
    return render_template('showJson.html')

@app.route('/getJson', methods=['GET'])
def getJson():
    return json.dumps(load_json())

if __name__ == '__main__':
    app.run()