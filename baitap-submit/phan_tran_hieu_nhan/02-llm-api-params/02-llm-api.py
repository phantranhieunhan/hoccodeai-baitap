from openai import OpenAI
import sys

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="random"
)

messages = []

is_stop = False

while not is_stop:
    print("You: ", end="", flush=True)
    user_input = sys.stdin.readline().strip()
    if user_input == "exit":
        is_stop = True
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    print(messages)
    print("--------------------------------")

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-oss-20b",
        stream=True
    )

    response = ""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
            response += chunk.choices[0].delta.content

    messages.append({
        "role": "assistant",
        "content": response
    })

    print()
    print("--------------------------------")

