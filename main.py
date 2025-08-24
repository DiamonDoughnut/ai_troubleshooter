import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
from functions.run_python import *
from functions.write_file import *
from functions.get_file_content import *

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories (get_files_info)
- Read file contents (get_file_content)
- Execute Python files with optional arguments (run_python_file)
- Write or overwrite files (write_file)

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    function_to_call = function_call_part.name
    args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_to_call}({args})")
    else:
        print(f" - Calling function: {function_to_call}")

    function_dict = {
        "get_files_info":get_files_info,
        "run_python_file":run_python_file,
        "get_file_content":get_file_content,
        "write_file":write_file
    }        

    if not function_to_call in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_to_call,
                    response={"error": f"Unknown function: {function_to_call}"}
                )
            ]
        )

    args["working_directory"] = "./calculator"

    result = function_dict[function_to_call](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_to_call,
                response={"result": result}
            )
        ]
    )


def main(prompt, verbose=False):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[available_functions]),
        )

    if response.function_calls:
        for call in response.function_calls:
            function_result = call_function(call, verbose=verbose)

            if not function_result.parts[0].function_response.response:
                raise Exception("Fatal Error: Something went wrong with the function call")
                exit(1)

            if verbose:
                print(f"-> {function_result.parts[0].function_response.response}")    


    print(response.text)

    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Troubleshooter")
    parser.add_argument(
        "user_prompt",
        type=str,
        help="The user's prompt sent to the AI. If it contains spaces, wrap it in quotes"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    args = parser.parse_args()
    main(args.user_prompt, args.verbose)
