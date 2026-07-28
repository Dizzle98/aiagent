import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified python file relative to the working directory, with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the python file to execute, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list[str]",
                    "description": "additional optional arguments to pass to the executing file",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        absolute_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_working_directory, file_path))

        valid_target_file = os.path.commonpath([absolute_working_directory, target_file]) == absolute_working_directory
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith("py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)
        process = subprocess.run(command, capture_output=True, timeout=30, text=True)

        output = ""
        return_code = process.returncode
        if not return_code == 0:
            output += f"Process exited with code {return_code}"

        if process.stdout is None and process.stderr is None:
            ouput += f"No output produced"
        else:
            output += f"STDOUT: {process.stdout} STDERR: {process.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
