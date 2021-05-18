# How to run Server?
## 1 Initialize the database, and create the database and table.
```shell
cd /workspace/papers_server
source venv/bin/activite
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### 2 Soft link PDF to app/static/PDF
```shell
ln PDF下载到的路径 项目文件夹/app/static/PDF
```
## 3 Run the service
```shell
python manage.py runserver -h 0.0.0.0 -p 5000
```
