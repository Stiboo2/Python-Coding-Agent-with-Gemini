import sys
import os
import requests
import json
from prompts import system_prompt

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

OLLAMA_URL = "http://localhost:11434/api/chat"
WORKING_DIR = "calculator"  # or wherever you want the files read from

def main():
    if len(sys.argv) < 2:
        print("I need a prompt")
        sys.exit(1)

    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True

    prompt = sys.argv[1]

    # All available functions for Ollama as plain dicts
    tools_payload = [
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]

    # Prepare the payload for Ollama
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

    # Check for tool calls
    if "tool_calls" in data["message"]:
        for tool_call in data["message"]["tool_calls"]:
            func_name = tool_call["function"]["name"]
            args = tool_call["function"]["arguments"]

            # Print the command the AI wants to call
            print(f"Calling function: {func_name}({args})")

            # Execute the function based on its name
            if func_name == "get_files_info":
                directory = args.get("directory", ".")
                result = get_files_info(WORKING_DIR, directory)
            elif func_name == "get_file_content":
                file_path = args.get("file_path", "")
                result = get_file_content(WORKING_DIR, file_path)
            elif func_name == "write_file":
                file_path = args.get("file_path", "")
                content = args.get("content", "")
                result = write_file(WORKING_DIR, file_path, content)
            elif func_name == "run_python_file":
                file_path = args.get("file_path", "")
                args_list = args.get("args", [])
                result = run_python_file(WORKING_DIR, file_path, args_list)
            else:
                result = f"Unknown function: {func_name}"

            print(f"\n[Function {func_name} Output]:\n{result}")
            return  # stop after first function call

    else:
        # Otherwise, just print the AI text
        print(data["message"]["content"])

    if verbose:
        print(f"\nUser prompt: {prompt}")
        print("(Ollama does not provide token counts)")

if __name__ == "__main__":
    main()
