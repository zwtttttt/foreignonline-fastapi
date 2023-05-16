# -*- encoding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2023/05/15 14:18:36
@Author  :   zwt 
@Version :   1.0
@Contact :   1030456532@qq.com
'''

# here put the import lib
import asyncio
import json
from configs.character import Character, get_character
from utils.utils import chat_stream, complex_messages, init_messages
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

app = FastAPI()
# 配置CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONTAINER = {}
RETRY_TIMEOUT = 15000  # milisecond

@app.get("/chat/{character}/{openid}/{message}")
async def chat(request: Request, character: Character, openid: str, message: str):
    character = get_character(character) # get the prompt of this character.
    if openid not in CONTAINER.keys(): CONTAINER[openid] = [init_messages("system", character), init_messages('user', character)]

    CONTAINER[openid] = complex_messages(CONTAINER[openid], message)
    response = chat_stream(CONTAINER[openid], 1000)
    
    async def generate():
         while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            data = init_messages("assistant", "")
            for r in response:
                if 'content' in r.choices[0].delta:
                    data['content'] += r.choices[0].delta['content']
                    yield r.choices[0].delta['content']
            
            CONTAINER[openid].append(data)
            break
        
    print(f"{openid}_{character}: {json.dumps(CONTAINER[openid], indent=4, sort_keys=True, ensure_ascii=False)}")

    return EventSourceResponse(generate())