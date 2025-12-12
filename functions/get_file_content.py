# functions/get_file_content.py
import os
from config import MAX_CHARS

# Actual function
def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'

    try:
        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
        if len(content) >= MAX_CHARS:
            content += f'\n[... File "{file_path}" truncated at {MAX_CHARS} characters ...]'
        return content
    except Exception as e:
        return f"Exception reading file: {e}"


# Ollama schema
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads a file in the working directory up to a max number of characters.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Relative path to the file."}
            },
            "required": ["file_path"]
        }
    }
}
