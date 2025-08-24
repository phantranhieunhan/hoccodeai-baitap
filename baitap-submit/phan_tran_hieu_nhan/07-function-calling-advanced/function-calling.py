import inspect
import os
from typing import Literal
from pydantic import BaseModel, Field, TypeAdapter
import requests
from dotenv import load_dotenv

load_dotenv()
JINA_TOKEN = os.getenv("JINA_TOKEN")


def get_current_weather(location: str, unit: Literal["celsius", "fahrenheit"]):
    """
    Get the current weather in a given location
    :param location: The city name
    :param unit: The temperature unit
    :output: the current weather information
    """

    return "Trời rét vãi nồi, 7 độ C"


def get_stock_price(symbol: str):
    """
    Get the current stock price of a given symbol
    """
    pass


def view_website(url: str):
    """
    View a website
    """
    jinaURL = "https://r.jina.ai/" + url
    headers = {"Authorization": "Bearer " + JINA_TOKEN}

    response = requests.get(jinaURL, headers=headers)
    return response.text


def function_to_model(func):
    sig = inspect.signature(func)

    annotations = {}
    fields = {}

    for name, param in sig.parameters.items():
        # type annotation
        annotations[name] = (
            param.annotation if param.annotation is not inspect._empty else str
        )

        # default or required
        if param.default is inspect._empty:
            fields[name] = Field(..., description=f"{name} parameter")
        else:
            fields[name] = Field(default=param.default, description=f"{name} parameter")

    # dynamically create model class
    return type(
        f"{func.__name__.capitalize()}Params",
        (BaseModel,),
        {"__annotations__": annotations, **fields},
    )


tools = [
    {
        "type": "function",
        "function": {
            "name": get_current_weather.__name__,
            "description": get_current_weather.__doc__.strip(),
            "parameters": TypeAdapter(
                function_to_model(get_current_weather)
            ).json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": get_stock_price.__name__,
            "description": get_stock_price.__doc__.strip(),
            "parameters": TypeAdapter(get_stock_price).json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": view_website.__name__,
            "description": view_website.__doc__.strip(),
            "parameters": TypeAdapter(view_website).json_schema(),
        },
    },
]

from pprint import pprint
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="random")
messages = [
    {
        "role": "user",
        "content": "Tóm tắt trang web này https://thanhnien.vn/dan-vu-khi-khi-tai-pho-dien-mot-phan-suc-manh-cua-luc-luong-vu-trang-viet-nam-18525082421225878.htm",
    }
]
print("Bước 1: Gửi message lên cho LLM")
pprint(messages)
print("===tools===")
pprint(tools)
response = client.chat.completions.create(
    model="openai/gpt-oss-20b", messages=messages, tools=tools
)
print("Bước 2: LLM đọc và phân tích ngữ cảnh LLM")
pprint(response)


print("Bước 3: Lấy kết quả từ LLM")
tool_call = response.choices[0].message.tool_calls[0]

pprint(tool_call)


import json

print("Bước 4: Chạy function get_current_weather ở máy mình")


# Vì ở đây ta có 3 hàm nên phải check theo name để gọi đúng hàm `get_current_weather`
if tool_call.function.name == "get_current_weather":
    arguments = json.loads(tool_call.function.arguments)
    weather_result = get_current_weather(
        arguments.get("location"), arguments.get("unit")
    )
    # Hoặc code này cũng tương tự
    # weather_result = get_current_weather(**arguments)
    print(f"Kết quả bước 4: {weather_result}")

    # Kết quả bước 4: Trời rét vãi nôi, 7 độ C

    print("Bước 5: Gửi kết quả lên cho LLM")
    messages.append(response.choices[0].message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": "get_current_weather",
            "content": weather_result,
        }
    )
    pprint(messages)

    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        # Ở đây không có tools cũng không sao, vì ta không cần gọi nữa
    )

    print(f"Kết quả cuối cùng từ LLM: {final_response.choices[0].message.content}.")
    # In kết quả ra
    # Kết quả cuối cùng từ LLM: Hôm nay ở Hà Nội trời rét, nhiệt độ khoảng 7 độ C. Bạn nên mặc ấm khi ra ngoài nhé!.

if tool_call.function.name == "view_website":
    arguments = json.loads(tool_call.function.arguments)
    web_content = view_website(arguments.get("url"))
    # Hoặc code này cũng tương tự
    # weather_result = get_current_weather(**arguments)
    print(f"Kết quả bước 4: {web_content}")

    # Kết quả bước 4: Trời rét vãi nôi, 7 độ C

    print("Bước 5: Gửi kết quả lên cho LLM")
    messages.append(response.choices[0].message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": "view_website",
            "content": web_content,
        }
    )
    pprint(messages)

    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        # Ở đây không có tools cũng không sao, vì ta không cần gọi nữa
    )

    print(f"Kết quả cuối cùng từ LLM: {final_response.choices[0].message.content}.")
    # In kết quả ra
