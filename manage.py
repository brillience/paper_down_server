#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/28 16:15
# @Author : ZhangXiaobo
# @Software: PyCharm
# 启动文件
"""
以脚本的形式管理爬虫，在开发阶段使用
例如：
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
"""
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models import Papers

app = create_app('development')
# 添加manage管理功能
manager = Manager(app)
# 添加数据库迁移功能
migrate = Migrate(app, db)

# 创建shell形势下，app的上下文
def make_shell_context():
    return dict(app=app, db=db, Papers=Papers)

# 添加shell command
manager.add_command("shell", Shell(make_context=make_shell_context))
# 添加shell command
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
