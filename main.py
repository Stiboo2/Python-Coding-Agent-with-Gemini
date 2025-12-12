import sys
import requests
import json
from prompts import system_prompt
from functions.get_files_info import get_files_info, schema_get_files_info

OLLAMA_URL = "http://localhost:11434/api/chat"
WORKING_DIR = "calculator"   # or wherever you want the files read from


def main():
    if len(sys.argv) < 2:
        print("I need a prompt")
        sys.exit(1)

    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True

    prompt = sys.argv[1]

    # Prepare the payload for Ollama
    payload = {
        "model": "llama3.2",  # change to your installed model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "tools": [schema_get_files_info],  # function calling
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
            args = tool_call["function"]["arguments"]  # already a dict

            # Print the command the AI wants to call
            print(f"Calling function: {func_name}({args})")

            # Execute the function if it's get_files_info
            if func_name == "get_files_info":
                directory = args.get("directory", ".")
                result = get_files_info(WORKING_DIR, directory)
                print(f"\n[Function {func_name} Output]:\n{result}")
                return

    # Otherwise, just print the AI text
    print(data["message"]["content"])

    if verbose:
        print(f"\nUser prompt: {prompt}")
        print("(Ollama does not provide token counts)")


if __name__ == "__main__":
    main()
