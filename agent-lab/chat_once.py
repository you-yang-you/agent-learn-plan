from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
resp=client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是耐心的编程助教，回答不超过100字，用中文。"},
        {"role": "user", "content": "什么是 API？用一句话解释。"},
    ],
)
print("回复：", resp.choices[0].message.content)
u = resp.usage
print(f"token用量：输入{u.prompt_tokens} / 输出 {u.completion_tokens}) / 总结 {u.total_tokens}")

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "我叫小明。"},
        {"role": "assistant", "content": "你好小明！"},
        {"role": "user", "content": "我叫什么名字？"},
    ],
)
print(resp.choices[0].message.content)
messages = []

print("==== DeepSeek 聊天程序（保留上下文记忆）====")
print("指令：exit 退出 | clear 清空对话历史\n")

while True:
    user_text = input("你：")
    user_text = user_text.strip()

    if user_text.lower() == "exit":
        print("AI：再见！")
        break
    if user_text.lower() == "clear":
        messages = []  # 清空历史
        print("AI：对话历史已清空，我们重新开始吧！\n")
        continue

    # 用户消息存入历史
    messages.append({"role": "user", "content": user_text})

    # 调用API，把全部历史传给模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    ai_reply = response.choices[0].message.content
    print(f"AI：{ai_reply}")

    # AI回复存入历史，维持上下文记忆
    messages.append({"role": "assistant", "content": ai_reply})

    # 打印token消耗
    usage = response.usage
    print(f"【Token统计】输入:{usage.prompt_tokens} 输出:{usage.completion_tokens} 总计:{usage.total_tokens}\n")
# 预期：模型能答出「小明」——因为它看到了前两轮历史
# 如果把中间那行 assistant 删掉，模型就答不上来：这就是上下文丢失
