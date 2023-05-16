# -*- encoding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2023/05/15 14:56:59
@Author  :   zwt 
@Version :   1.0
@Contact :   1030456532@qq.com
'''

# here put the import lib
import openai
from configs.GPT import GPT_CONFIG


def chat_stream(messages: list, max_tokens: int):
    openai.api_key = GPT_CONFIG.API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=max_tokens,
        stream=True,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        user='foreign online'
    )
    return response


def complex_messages(old: list, new: str):
    new = {"role": "user", "content": new}
    old.append(new)
    return old

def init_messages(role: str, content: str):
    return {
        "role": role,
        "content": content
    }
