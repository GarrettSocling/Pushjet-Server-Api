#!/usr/bin/env python2.7
# coding=utf-8
from __future__ import unicode_literals
from flask import Flask, jsonify, redirect, send_from_directory
from shared import db, limiter, sockets
from controllers import *
from utils import Error
from sys import exit, stderr

try:
    import config
except ImportError:
    stderr.write("Please copy config.example.py to config.py and edit the file.")
    exit(1)

if config.google_api_key == '':
    stderr.write("GCM disabled, please enter the google api key for gcm")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.database_uri
db.init_app(app)
limiter.init_app(app)
sockets.init_app(app)
limiter.enabled = config.limiter


@app.route('/')
def index():
    return redirect('/docs/')


@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')


@app.errorhandler(429)
def limit_rate(e):
    return jsonify(Error.RATE_TOOFAST)


app.register_blueprint(listen)
app.register_blueprint(message)
app.register_blueprint(service)
app.register_blueprint(docs)
if config.google_api_key is not "":
    app.register_blueprint(gcm)

if __name__ == '__main__':
    app.debug = True
    app.run()