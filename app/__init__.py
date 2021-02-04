#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 15:56
# @Author : ZhangXiaobo
# @Software: PyCharm
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_bluprient
    app.register_blueprint(main_bluprient)

    return app


