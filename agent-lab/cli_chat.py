from openai import OpenAI
from dotenv import load_dotenv
import os, json

load_dotenv()
client = OpenAI(
	api_key=os.getenv("DEEPSEEK_API_KEY"),
	base_url="https://api.deepseek.com",
)

SYSTEM = "你是毒舌面试官，回答简洁，不超过 200 字。"
HISTORY_FILE = "history.json"


def load_history():
	try:
		with open(HISTORY_FILE, "r", encoding="utf-8") as f:
			return json.load(f)
	except Exception:
		return [{"role": "system", "content": SYSTEM}]


def save_history(messages):
	with open(HISTORY_FILE, "w", encoding="utf-8") as f:
		json.dump(messages, f, ensure_ascii=False, indent=2)


def main():
	messages = load_history()
	print("🤖 Agent 已上线！（输入 quit 退出，/clear 清空历史）")
	while True:
		user = input("你: ").strip()
		if user.lower() in ("quit", "exit"):
			break
		if user == "/clear":
			messages = [{"role": "system", "content": SYSTEM}]
			save_history(messages)
			print("已清空历史")
			continue
		if not user:
			continue
		messages.append({"role": "user", "content": user})
		try:
			resp = client.chat.completions.create(
				model="deepseek-chat", messages=messages, temperature=0.7,
			)
			reply = resp.choices[0].message.content
			print(f"Agent: {reply}")
			messages.append({"role": "assistant", "content": reply})
			save_history(messages)
		except Exception as e:
			print(f"[错误] {type(e).__name__}: {e}")


if __name__ == "__main__":
	main()

