#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai_api_key = os.environ['OPENAI_API_KEY']

from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def gen_gpt_messages(prompt):
    messages = [{"role": "user", "content": prompt}]
    return messages


def get_completion(prompt, model="gpt-3.5-turbo", temperature = 0):
    response = client.chat.completions.create(
        model=model,
        messages=gen_gpt_messages(prompt),
        temperature=temperature,
    )
    if len(response.choices) > 0:
        return response.choices[0].message.content
    return "generate answer error"

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature = 0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    if len(response.choices) > 0:
        return response.choices[0].message.content
    return "generate answer error"

def get_completion_and_token_count(messages, 
                                   model="gpt-3.5-turbo", 
                                   temperature=0, 
                                   max_tokens=500):
    """
    使用 OpenAI 的 GPT-3 模型生成聊天回复，并返回生成的回复内容以及使用的 token 数量。

    参数:
    messages: 聊天消息列表。
    model: 使用的模型名称。默认为"gpt-3.5-turbo"。
    temperature: 控制生成回复的随机性。值越大，生成的回复越随机。默认为 0。
    max_tokens: 生成回复的最大 token 数量。默认为 500。

    返回:
    content: 生成的回复内容。
    token_dict: 包含'prompt_tokens'、'completion_tokens'和'total_tokens'的字典，分别表示提示的 token 数量、生成的回复的 token 数量和总的 token 数量。
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    if len(response.choices) > 0:
        result = response.choices[0].message.content
        token_dict = {
            'prompt_tokens':response.usage.prompt_tokens,
            'completion_tokens':response.usage.completion_tokens,
            'total_tokens':response.usage.total_tokens,
        }
        return result, token_dict
    return "generate answer error"