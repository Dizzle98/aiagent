import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_working_directory, directory))

        valid_target_dir = os.path.commonpath([absolute_working_directory, target_dir]) == absolute_working_directory
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f'Error: "{e}"'

    try:
        dir_content = os.listdir(target_dir)
        results = [f"Result for '{directory}' directory:"]
        for content in dir_content:
            file_name = content
            file_size = os.path.getsize(os.path.join(target_dir, file_name))
            is_directory = os.path.isdir(os.path.join(target_dir, file_name))
            results.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_directory}")
    except Exception as e:
        return f'Error: "{e}"'

    result = f"{file_name}: file_size={file_size} bytes, is_dir={is_directory}"

    return "\n".join(results) #f'Success: "{directory}" is within the working directory'