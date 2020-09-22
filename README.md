# 质量工具后端
### 安装pipenv
```
pip install pipenv
```

### 使用pipenv生成虚拟环境安装依赖，并且进入虚拟环境
```
pipenv install
pipenv shell
```

### 注意！！！
- pipenv装不上部分依赖,必须在虚拟环境下运行以下命令才能正常安装

```
pip install opencv-python -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install numpy -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
pip install pillow  -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
```

### 库迁移

```
python manage.py makemigrations
python manage.py migrate

# insert配置项sql
INSERT INTO camus_config (id, c_key, c_value, remark, gmt_created, gmt_modified) VALUES (1, 'project_status', '[{"status":0, "label":"进行中"},{"status":1, "label":"已完成"},{"status":-1, "label":"已关闭"}]', null, '2020-04-07 08:34:02.543364', '2020-04-07 08:34:02.543364');
INSERT INTO camus_config (id, c_key, c_value, remark, gmt_created, gmt_modified) VALUES (2, 'project_progress_app', '[{"status":0,"label":"营销助手"},{"status":1,"label":"业务报表-儿绘赛业务报表"},{"status":2,"label":"一键投保"},{"status":3,"label":"中台-承保-问卷"},{"status":4,"label":"保全-短期险续保"},{"status":5,"label":"短信发送"},{"status":6,"label":"核心-微信代理接口"}]', null, '2020-04-07 08:34:02.543364', '2020-04-07 08:34:02.543364');
INSERT INTO camus_config (id, c_key, c_value, remark, gmt_created, gmt_modified) VALUES (3, 'project_progress_stage', '[{"status":0,"label":"需求评审"},{"status":1,"label":"测分设计"},{"status":2,"label":"测分评审"},{"status":3,"label":"编写用例"},{"status":4,"label":"用例评审"},{"status":5,"label":"功能测试"},{"status":6,"label":"回归测试"},{"status":7,"label":"待上线"},{"status":8,"label":"已上线"},{"status":9,"label":"等待提测"}]', null, '2020-04-07 08:34:02.543364', '2020-04-07 08:34:02.543364');
```
### 启动服务
```
# 端口要改成4396
python manage.py runserver 4396
```
