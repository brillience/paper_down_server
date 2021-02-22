#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 16:57
# @Author : ZhangXiaobo
# @Software: PyCharm

"""
项目的配置文件，web配置信息和爬虫配置信息，在此设置
"""

# 爬虫pdf保存地址
WOS_CRAWLER_FILES_STORE = r'/home/zxb/store/PDF'
# web与爬虫相关数据库信息
DB_PATH = "mysql+pymysql://root:123456@127.0.0.1:3036/papers_server"


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # 数据库信息
    SQLALCHEMY_DATABASE_URI = DB_PATH
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
