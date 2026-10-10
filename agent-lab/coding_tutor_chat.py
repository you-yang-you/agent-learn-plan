import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# 初始化：固定系统角色，只写一次！
messages = [
    {"role": "system", "content": "你是耐心的编程助教，回答不超过100字，用中文。"}
]

print("==== DeepSeek 编程助教 ====")
print("指令：exit 退出 | clear 清空对话历史（系统角色仍保留）\n")

while True:
    user_text = input("你：")
    user_text = user_text.strip()

    if user_text.lower() == "exit":
        print("AI：再见！")
        break
    if user_text.lower() == "clear":
        # 清空用户/助手对话，但保留system角色！
        messages = [messages[0]]
        print("AI：对话历史已清空，我们重新开始！\n")
        continue

    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    ai_reply = response.choices[0].message.content
    print(f"AI：{ai_reply}")
    messages.append({"role": "assistant", "content": ai_reply})

    usage = response.usage
    print(f"【Token统计】输入:{usage.prompt_tokens} 输出:{usage.completion_tokens} 总计:{usage.total_tokens}\n")