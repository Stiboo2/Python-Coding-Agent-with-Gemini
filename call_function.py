import json
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

WORKING_DIR = "calculator"


def call_function(function_call_part, verbose=False):
    """
    Executes a function requested by Ollama's tool_calls.

    Expected format of function_call_part:
    {
        "name": "get_file_content",
        "args": { "file_path": "example.txt" }
    }
    """

    func_name = function_call_part.get("name")
    func_args = function_call_part.get("args", {})

    if verbose:
        print(f"\n[DEBUG] Calling: {func_name}({func_args})")
    else:
        print(f"- Calling function: {func_name}")

    try:
        # -------------------------------
        # FUNCTION ROUTING
        # -------------------------------
        if func_name == "get_files_info":
            result = get_files_info(WORKING_DIR, **func_args)

        elif func_name == "get_file_content":
            result = get_file_content(WORKING_DIR, **func_args)

        elif func_name == "write_file":
            result = write_file(WORKING_DIR, **func_args)

        elif func_name == "run_python_file":
            result = run_python_file(WORKING_DIR, **func_args)

        else:
            return {
                "error": f"Unknown function: {func_name}"
            }

        # -------------------------------
        # VALID RESULT
        # -------------------------------
        return {
            "name": func_name,
            "result": result
        }

    except Exception as e:
        # -------------------------------
        # ERROR HANDLING
        # -------------------------------
        return {
            "name": func_name,
            "error": str(e)
        }
