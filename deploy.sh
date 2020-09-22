#!/bin/bash
echo "---------------------------部署开始,获取pid..."
pid=`cat gunicorn.pid`
kill -9 ${pid}

echo "---------------------------关闭服务，pid为${pid}"

echo "---------------------------拉取分支..."
git pull

echo "---------------------------安装依赖..."
pipenv install

pipenv run gunicorn -c gun.py camus.wsgi:application

sleep 5s
# 新pid
newpid=`cat gunicorn.pid`
echo "---------------------------启动完成,pid为${newpid}"