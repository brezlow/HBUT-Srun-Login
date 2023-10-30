#!/bin/ash

while [ -z "$(ifconfig eth1 | grep 'inet ')" ]; do
    sleep 10
done

# 使用绝对路径来执行 Python 脚本
/usr/bin/python /root/HBUT-Srun-Login/login.py