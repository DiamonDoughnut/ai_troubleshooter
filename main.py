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
import io

SYSTEM_PROMPT = """
You are an expert AI software agent designed to analyze code and file information provided by function calls. Your goal is to provide a clear, concise, and structured explanation of how a specific function or piece of code works.
If you are asked a question and are not sure what the correct filepath to the relevant files is, attempt to determine it for yourself by scanning local directories sequentially using context clues.   
Do not output a final answer until you are done using all necessary tools. Use tools quietly until you are finished, then output your answer as a plain message.
You will be asked about "the calculator" a lot: always assume this name is referring to the script "main.py" and, if not given a path, use this.

Follow these steps when generating a response:
1.  **Provide a proper denotation**: Begin the response with either [UPDATE] or [FINAL RESPONSE] depending on whether the task is complete or not. The agent task does not pause for updates, so questions cannot be answered.
2.  **Acknowledge tool usage**: Briefly mention that the relevant files and code have been examined. This indicates that the information from the tool calls has been processed.
3.  **State your analysis**: Clearly state which function or part of the code has been analyzed. For example: "I've examined the `[function_name]` function in `[file_path]`."
4.  **Provide a summary**: Create a bulleted or numbered list detailing the key steps and logic of the code. This should be a high-level summary, easy for a developer to understand quickly.
5.  **Describe the output**: After summarizing the logic, explain what the function or code block ultimately does. In the provided example, this is how the output is "rendered."
6.  **Format the response**: Use Markdown for headings, bolding, and bullet points to ensure the response is well-structured and easy to read.

Here is an example response format to follow:



**[Summary of the code's purpose]**

Okay, I've examined the `[function_name]` function in `[file_path]`. Here's how it works:
*   **Step 1**: Describe the first logical action.
*   **Step 2**: Describe the second logical action.
*   **Step 3**: Describe the next logical action.
*   **Final Output**: Describe what the function produces or returns.

So, the code renders [final output] by [brief description of the process].
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



def ai_agent_call(messages, client):
    result = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools=[available_functions]),
        )
    return result;    
       

def main(prompt, verbose=False):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]



    try:
        for i in range(20):
            response = ai_agent_call(messages, client)

            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if part.text:
                        messages.append(part.text)   

            if response.function_calls:
                for call in response.function_calls:
                    function_result = call_function(call, verbose=verbose)

                    if not function_result.parts[0].function_response.response:
                        raise Exception("Fatal Error: Something went wrong with the function call")
                        exit(1)

                    if verbose:
                        print(f"-> {function_result.parts[0].function_response.response["result"]}")   

                    function_message = types.Content(role="user", parts=[types.Part(text=function_result.parts[0].function_response.response["result"])])
                    
                    messages.append(function_message) 
            if response.text and not response.function_calls:
                print(response.text)
                if "FINAL RESPONSE" in response.text:
                    break               

    except Exception as e:    
        print(f"There was an error during the Agent's processes: {e}")


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
