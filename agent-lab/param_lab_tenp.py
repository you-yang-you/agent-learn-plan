import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

PROMPT ="写一句关于秋天的话，20字左右。"
for temp in (1.5 ,0, 0.7,):
    for i in range(2):
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": PROMPT}],
                temperature=temp, max_tokens=50,
        )
        print(f"temp={temp}, # {i+1}: {resp.choices[0].message.content}")



