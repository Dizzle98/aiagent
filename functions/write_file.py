import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_working_directory, file_path))

        valid_target_file = os.path.commonpath([absolute_working_directory, target_file]) == absolute_working_directory
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent = os.path.dirname(target_file)
        os.makedirs(parent, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: "{e}"'