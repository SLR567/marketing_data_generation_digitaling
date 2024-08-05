from openai import OpenAI
import os
import json

def get_response(prompt):
    client = OpenAI(
        api_key="sk-34ced28392f749c7938b63906daf88e4", 
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", 
    )
    completion = client.chat.completions.create(
        model="qwen2-1.5b-instruct",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}],
        temperature=0.8,
        top_p=0.8
        )
    output = json.loads(completion.model_dump_json())
    output_final = output["choices"][0]["message"]["content"]
    return output_final