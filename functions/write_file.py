import os

def write_file(working_directory, file_path, content):
    permitted_wd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(permitted_wd, file_path))

    if not full_path.startswith(permitted_wd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
        except Exception as ex:
            return f'Error: creating directory {ex}'
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:
        with open(full_path, "w") as file:
            file.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as ex:
        return f'Error: writing file: {ex}'
