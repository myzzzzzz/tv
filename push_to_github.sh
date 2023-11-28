#!/bin/bash
cd /root/epg/download/Git
# 首先执行 git pull 拉取远程仓库的变更
git pull origin master
# 然后添加文件、提交并推送更改
git add zzz.xml
git commit -m "Auto commit at $(date +'%Y-%m-%d %H:%M:%S')"
git push origin master