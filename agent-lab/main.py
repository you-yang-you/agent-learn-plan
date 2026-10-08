from openai import OpenAI
from dotenv import load_dotenv
import os


def main():
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("未找到 DEEPSEEK_API_KEY，请先在 .env 文件中配置该变量。")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "请用一句话介绍自己。"}],
        )

        content = resp.choices[0].message.content
        if content:
            print(content)
        else:
            print("模型未返回内容。")
    except Exception as exc:
        print(f"请求失败: {exc}")
        raise


if __name__ == "__main__":
    main()   
