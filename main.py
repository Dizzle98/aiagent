import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("no API_KEY found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose ouput")
    args = parser.parse_args()

    client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key = api_key
    )

    messages = [
        {
            "role": "system", 
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    response = generate_content(client, messages)

    message = response.choices[0].message
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call)
        if result_message["content"] is None:
            raise Exception("No content in result found")
        if args.verbose:
            print(f"-> {result_message["content"]}")
        #print(f"Calling function: {tool_call.function.name}({function_args})")

    if args.verbose:
        print(f"User prompt: {messages[0]["content"]}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print(f"Response: {response.choices[0].message.content}")
    

def generate_content(client, messages):
    response = client.chat.completions.create(
        model="openrouter/free", 
        messages=messages,
        tools=available_functions,
    )
    if response.usage is None:
        raise RuntimeError("failed API request")
    return response


if __name__ == "__main__":
    main()
