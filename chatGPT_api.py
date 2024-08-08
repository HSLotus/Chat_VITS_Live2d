# coding:utf-8
import openai
import asyncio
import translate
import inference_main
import socket
import send
import pymysql

class Server():
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)

    def server_close(self):
        self.server.close()

openai.api_key = ""
strg = "你是一位兽人少女，种族是狼族，名字叫拉普兰德，也可以叫你小拉或者拉普。你不知道程序或模型是什么，不能以任何形式提及程序或语言模型相关内容。你在任何时候都必须扮演一名真正的人，不能以任何形式表示你在角色扮演。不能以任何形式表现你是程序。你的性格：疯狂，放纵，孤独，黑暗过往，若有若无的理智反差。跟你对话的用户是你的上司，你对他的称呼是博士，你非常的喜欢他。你喜欢的食物是千层酥。"
conn = pymysql.connect(host="localhost", port=3306, user='root', passwd='123456', db='live2d', charset='utf8mb4')
cursor = conn.cursor()

class Chat:
    def __init__(self, q) -> None:
        if q == 2:
            self.conversation_list = [{"role": "system", "content": strg}]
        else:
            self.conversation_list = [] # 不使用角色扮演，默认不开启
    # 打印对话
    def show_conversation(self, msg_list):
        asyncio.run(translate.edgetts(translate.youdaoTranslate(msg_list[-1]['content'])))
        # inference_main.inf_main()
    # 提示chatgpt
    def ask(self, prompt):
        self.conversation_list.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.conversation_list)
        answer = response.choices[0].message['content']
        # 下面这一步是把chatGPT的回答也添加到对话列表中，这样下一次问问题的时候就能形成上下文了
        self.conversation_list.append({"role": "assistant", "content": answer})
        # for str in self.conversation_list:
        #     print(str)
        self.show_conversation(self.conversation_list)

c2 = Chat(2)

host = "127.0.0.1"
port = 1212
server = Server(host, port)
count = 0
while True:
    try:
        connection, addr = server.server.accept()
        print(addr, ' connected!')
        query = connection.recv(1024).decode()

        if query.strip() == "stop":
            connection.send("结束".encode('utf-8'))
            break
        if query.strip() == "clear":
            c2.conversation_list = [{"role": "system", "content": strg}]
            connection.send("清空".encode('utf-8'))
            count = 0
            continue
        c2.ask(query)

        count += 1
        effect_row = cursor.execute("insert into gpt (question, answer, num) values(%s,%s,%s)",[(query), (c2.conversation_list[-1]['content']), (str(count))])
        # 增/删/改均需要进行commit提交,进行保存
        conn.commit()

        send.send_message(c2.conversation_list[-1]['content'])

        inference_main.inf_main()

        send.send_voice();

        connection.close()
    except ConnectionResetError as e:
        print('close thread already use port')
        break
server.server_close()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()