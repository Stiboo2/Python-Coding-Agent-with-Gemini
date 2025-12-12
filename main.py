import sys
import os
import requests
import json
from prompts import system_prompt

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

from call_function import call_function

OLLAMA_URL = "http://localhost:11434/api/chat"
WORKING_DIR = "calculator"


def main():
    if len(sys.argv) < 2:
        print("I need a prompt")
        sys.exit(1)

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    # All tools as dict schemas
    tools_payload = [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]

    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "tools": tools_payload,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        print("Error:", response.text)
        return

    data = response.json()

    # Verbose: Print prompt + token usage (Ollama does NOT provide token counts)
    if verbose_flag:
        print(f"User prompt: {prompt}")
        print("Prompt tokens: (not available in Ollama)")
        print("Response tokens: (not available in Ollama)")

    # ---------------------------------------------
    # HANDLE FUNCTION CALLS
    # ---------------------------------------------
    message = data.get("message", {})

    if "tool_calls" in message:
        for tool_call in message["tool_calls"]:
            func = {
                "name": tool_call["function"]["name"],
                "args": tool_call["function"]["arguments"]
            }

            # Let the unified handler execute the function
            result = call_function(func, verbose_flag)

            # Print function execution result
            print(f"\n[Function {func['name']} Output]:")
            print(result)

        return  # Stop after tool execution

    # ---------------------------------------------
    # OTHERWISE PRINT NORMAL TEXT
    # ---------------------------------------------
    print(message.get("content", ""))


if __name__ == "__main__":
    main()
