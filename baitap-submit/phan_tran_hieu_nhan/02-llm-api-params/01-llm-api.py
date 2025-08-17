from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="random"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Hello. Who are you?"
        }
    ],
    model="openai/gpt-oss-20b",
    stream=True
)

for chunk in chat_completion:
    print(chunk.choices[0].delta.content, end="", flush=True)