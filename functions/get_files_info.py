import os

def get_files_info(working_directory, directory=None) -> str:
    permitted_wd = os.path.abspath(working_directory)
    target_dir = permitted_wd

    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(permitted_wd):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    try:
        directory_contents = os.listdir(target_dir)
        formatted_directory_contents = []
        for content in directory_contents:
            content_path = os.path.join(target_dir, content)
            file_size = 0
            is_dir = os.path.isdir(content_path)
            file_size = os.path.getsize(content_path)

            formatted_directory_contents.append(f"- {content}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(formatted_directory_contents)
    except Exception as ex:
        return f"Error listing files: {ex}"
