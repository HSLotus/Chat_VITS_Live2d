import socket
import time


def send_message(str):
    ip_addr = ("127.0.0.1", 8888)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ip_addr)
    client.send(str.encode('utf-8'))
    client.close()

def send_voice():
    ip_addr = ("127.0.0.1", 8888)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ip_addr)

    filedir = "results/out.wav_auto_Lapland.flac"

    total = 0
    with open(filedir, "rb") as f:
        for line in f:
            client.send(line)
            total += len(line)
        print("文件发送完成，总大小：" + str(total) + "字节")

    client.close()

if __name__ == "__main__":
    send_message("hello world")
    time.sleep(5)
    send_voice()
