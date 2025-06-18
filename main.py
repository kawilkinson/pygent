import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from system_prompt import system_prompt

def main():
    load_dotenv()
    if len(sys.argv) > 1:
        if sys.argv[-1] == "--verbose":
            is_verbose = True
            prompt = " ".join(sys.argv[1:-1])
        else:
            is_verbose = False
            prompt = " ".join(sys.argv[1:])
    else:
        print("No prompt provided, exiting the program")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    if is_verbose:
        print(f"User Prompt: {prompt}")

    generate_ai_content(client, messages, is_verbose)


def generate_ai_content(client, messages, is_verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    if is_verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

    if not response.function_calls:
        return response.text
    
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

if __name__=="__main__":
    main()
