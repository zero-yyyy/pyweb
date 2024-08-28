"""
Author : book
Time   : 2024/5/22 下午5:22
File   : server_conf.py
"""
from flask import Flask, redirect, render_template, request, session, url_for
import pymysql

# 数据库连接参数
db_config = {
    'host': '127.0.0.1', 
    'user': 'root',         #数据库用户名
    'passwd': '123456',     #用户密码
    'db': 'book',           #数据库的名字
    'port': 3306,           #端口号
    'charset': 'utf8'       #编码方式
}

# 创建数据库连接
def create_connection():
    return pymysql.connect(**db_config)
