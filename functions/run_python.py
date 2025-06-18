import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    permitted_wd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(permitted_wd, file_path))

    if not full_path.startswith(permitted_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python", full_path]
        if args:
            commands.extend(args)

        result = subprocess.run(
            commands, 
            cwd=permitted_wd, 
            capture_output=True, 
            text=True, 
            timeout=30.0
            )

        output = []
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        
        if output:
            return "\n".join(output)
        else:
            return "No output produced"

    except Exception as ex:
        return f'Error: executing Python file {ex}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified .py file with optional arguments as long as it is in the permitted working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The .py file to run code from, the code may only make changes within the permitted working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The optional arguments provided, if none given then this value stays None",
            )
        }
    )
)
