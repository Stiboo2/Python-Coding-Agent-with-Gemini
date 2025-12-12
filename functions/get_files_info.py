import os

def get_files_info(working_directory, directory="."):
    abs_work_dir = os.path.abspath(working_directory)
    abs_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_work_dir):
        return f'Error: "{directory}" is outside working directory'

    final_response = ""
    contents = os.listdir(abs_directory)

    for content in contents:
        content_path = os.path.join(abs_directory, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f"- {content}: file_size={size} bytes, is_dir={is_dir}\n"

    return final_response


# ---- Ollama function schema ----
# get_files_info schema
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a directory within the working folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory to scan, relative to working folder."
                }
            },
            "required": []
        }
    }
}

# Similar dicts for schema_get_file_content, schema_write_file, schema_run_python_file
