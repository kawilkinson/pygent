import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

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


    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
    )


    if is_verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print("No --verbose flag detected")

if __name__=="__main__":
    main()
