#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 16:15
# @Author : ZhangXiaobo
# @Software: PyCharm
# 启动文件
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models import Papers

app = create_app('production')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Papers=Papers)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
