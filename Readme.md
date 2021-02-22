# Run Server
## 1 初始化数据库，并创建数据库和表
```shell
cd /workspace/papers_server
source venv/bin/activite
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### 2 将PDF软连接到app/static/PDF
```shell
ln PDF下载到的路径 项目文件夹/app/static/PDF
```
## 3 运行服务
```shell
python manage.py runserver -h 0.0.0.0 -p 5000
```