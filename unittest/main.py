# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :main.py
# @Time      :2022/9/29 12:18
# @Author    :JefferyH
from flask_cors import *
from flask import Flask, request, jsonify, session, Response,Config,make_response

app = Flask(__name__)

@app.route("/api/use",methods=['POST'])

def use():
    info = request.json['info']
    print('{:=^15}\n姓名：{}\n学院：{}\n专业：{}'.format("学生信息", info['realName'], info['orgName'],
                                                      info['specialtyName']))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="3600", debug=True)