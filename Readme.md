# Run Server
## 1 初始化数据库，并创建数据库和表
```shell
cd /workspace/papers_server
source venv/bin/activite
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
## 2 运行服务
```shell
python manage.py runserver -h 0.0.0.0 -p 5000
```