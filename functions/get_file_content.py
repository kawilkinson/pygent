import os

def get_file_content(working_directory, file_path):
    permitted_wd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(permitted_wd, file_path))

    if not full_path.startswith(permitted_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        MAX_CHARS = 10000
        with open(full_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
        
        if len(file_content_string) >= 10000:
            file_content_string += f'...File "{file_path}" truncated at 10000 characters'

        return file_content_string
        
    except Exception as ex:
        return f'Error reading file "{file_path}": {ex}'
