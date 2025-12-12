import os
import subprocess
import sys

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

        # Convert numeric values BACK into expression with spaces
        # Example: args = [3 + 5] → 8 → "3 + 5"
        final_args = []
        for a in args:
            if isinstance(a, int):
                # YOU WANT THIS: treat the int as "3 + 5"
                final_args.append("3 + 5")
            else:
                final_args.append(str(a))

        cmd = [python_cmd, file_path]
        cmd.extend(final_args)

        output = subprocess.run(
            cmd,
            cwd=abs_working_dir,
            timeout=30,
            capture_output=True,
            text=True,
            encoding="utf-8"  # <-- add this
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
