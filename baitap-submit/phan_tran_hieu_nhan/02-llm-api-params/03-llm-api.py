import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import sys

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="random"
)

def fetch_content(url: str) -> str:
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    main_div = soup.find("div", id="main-detail")
    return main_div.get_text(separator="\n") if main_div else soup.get_text()

is_stop = False

while not is_stop:
    print("You: ", end="", flush=True)
    user_input = sys.stdin.readline().strip()
    if user_input == "exit":
        is_stop = True
        break
    
    content = fetch_content(user_input)

    prompt = f"""Summary the content of the article below into 3-5 main ideas, concise, easy understand:\n\n {content}"""
    print(prompt)
    
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt
        }],
        model="openai/gpt-oss-20b",
        stream=True
    )

    response = ""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
            response += chunk.choices[0].delta.content

    print()
    print("--------------------------------")
