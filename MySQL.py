#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2018/5/13

import pymysql

# 创建连接
conn = pymysql.connect(host="localhost", port=3306, user='root', passwd='123456', db='live2d', charset='utf8mb4')
cursor = conn.cursor()

str1 = "你好"
str2 = "你好，我是chatgpt"
str3 = "こんにちは,chatgptです"
id = 27

effect_row = cursor.execute("insert into gpt (question, answer, translation, num) values(%s,%s,%s,%s)",[(str1),(str2),(str3),(str(id))])

# 增/删/改均需要进行commit提交,进行保存
conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()

# INSERT INTO EMPLOYEE(FIRST_NAME,LAST_NAME, AGE, SEX, INCOME) VALUES ('Mac', 'Mohan', 20, 'M', 2000)