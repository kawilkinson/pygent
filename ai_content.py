from google.genai import types
from config import ai_functions
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from system_prompt import system_prompt

def generate_ai_content(client, prompt, is_verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    i = 0
    while i < 20:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)

        if is_verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

        if not response.function_calls:
            return response.text
        
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, is_verbose)
            messages.append(function_call_result)
            if function_call_result.parts[0].function_response.response:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                raise ValueError("No response found from function call result.")
        
        i += 1
    
    return response.text


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_call_part.name in ai_functions:
        ai_function = ai_functions[function_name]
        function_result = ai_function("./calculator", **function_args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )