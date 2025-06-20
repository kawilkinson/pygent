import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from ai_content import generate_ai_content

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

    if is_verbose:
        print(f"User Prompt: {prompt}")

    # Print out the response at the end of the feedback loop from the Gemini agent
    print(generate_ai_content(client, prompt, is_verbose))

if __name__=="__main__":
    main()
