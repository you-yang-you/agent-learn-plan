import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

resp = client.chat.completions.create(
	model="deepseek-chat",
	messages=[{"role": "user", "content": "写一段 150 字左右的自我介绍"}],
	max_tokens=20,
	temperature=0.7,
	stream=True,               # 开启流式
)
print("Agent: ", end="", flush=True)
for chunk in resp:
	delta = chunk.choices[0].delta.content
	if delta:
		print(delta, end="", flush=True)   # 逐字打印，打字机效果
print()