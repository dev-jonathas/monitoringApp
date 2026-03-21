import os
from openai import AzureOpenAI
from prompts.systemPrompt import Prompts
import json

client = AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint="https://gpt-monitoring-app.openai.azure.com/",
        api_key=os.environ.get("OPEN_AI_KEY"),
)

def chamarOpenAi(obj: dict) -> str:
    response = client.chat.completions.create(
    
    
    messages=[
        {
            "role": "system",
            "content": Prompts.PROMPTV1,
        },
        {
            "role": "user",
            "content": json.dumps(obj),
        }
    ],
    max_completion_tokens=13107,
    temperature=1.0,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    model="gpt-4.1-mini"
    )

    return(response.choices[0].message.content)

