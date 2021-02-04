#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 16:57
# @Author : ZhangXiaobo
# @Software: PyCharm


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3036/papers_server"
    SECRET_KEY = 'TPmi4aLWRbyVq8zu9v82dWYW1'
    BOOTSTRAP_SERVE_LOCAL = True
    BOOTSTRAP_USE_MINIFIED = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True



class TestingConfig(Config):
    TESTING = True
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
