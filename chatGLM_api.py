import asyncio
import translate
from transformers import AutoTokenizer, AutoModel
import signal
import playsound
import inference_main

stop_stream = False

def signal_handler(signal, frame):
    global stop_stream
    stop_stream = True

tokenizer = AutoTokenizer.from_pretrained("model_int4", trust_remote_code=True)
model = AutoModel.from_pretrained("model_int4", trust_remote_code=True).half().cuda()
model = model.eval()

def main():
    global stop_stream
    history = []
    res_end = ""
    print("欢迎使用 ChatGLM-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
    while True:
        query = input("\n用户：")
        if query.strip() == "stop":
            break
        if query.strip() == "clear":
            print("已清空缓存")
            history = []
            continue
        count = 0
        for response, history in model.stream_chat(tokenizer, query, history=history):
            if stop_stream:
                stop_stream = False
                break
            else:
                count += 1
                res_end = response
                if count % 8 == 0:
                    signal.signal(signal.SIGINT, signal_handler)
        asyncio.run(translate.edgetts(translate.youdaoTranslate(res_end)))
        inference_main.inf_main()

if __name__ == "__main__":
    main()

