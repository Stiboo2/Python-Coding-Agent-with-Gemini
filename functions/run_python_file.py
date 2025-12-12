import os
import subprocess
import sys
import json

# Function to run Python files safely
def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: "{file_path}" is not in the working directory.'

    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        python_cmd = sys.executable

        # Ensure args is a list
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                args = [args]

        # Convert all args to strings
        final_args = [str(a) for a in args]

        # Run with unittest module for test files
        cmd = [python_cmd, "-m", "unittest", file_path] + final_args

        output = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

        result = f"""
***
STDOUT:
{output.stdout}

STDERR:
{output.stderr}
***
"""

        if output.stdout == "" and output.stderr == "":
            result = "No output produced.\n"

        if output.returncode != 0:
            result += f"Process exited with code {output.returncode}\n"

        return result

    except Exception as e:
        return f"Error executing Python file: {e}"


# Ollama function schema as a dict (JSON-serializable)
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file inside a given working directory with optional arguments, and returns stdout/stderr.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative path of the Python file to execute inside the working directory."
                },
                "args": {
                    "type": "array",
                    "description": "Optional list of arguments to pass to the Python file.",
                    "items": {"type": "string"}
                }
            },
            "required": ["file_path"]
        }
    }
}
