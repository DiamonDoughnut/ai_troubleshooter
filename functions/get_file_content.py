from pathlib import Path
from google.genai import types

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        working_dir = Path(working_directory).resolve()
        target_file = (working_dir / file_path).resolve()

        if not target_file.is_relative_to(working_dir):
            raise ValueError(f"Error: cannot read {file_path} as it is outside the permitted working directory")
        if not target_file.is_file():
            raise ValueError(f"Error: File not found or is not a regular file: {file_path}")

        file_size = target_file.stat().st_size
        is_truncated = file_size > MAX_CHARS

        with target_file.open(mode="r", encoding="utf-8") as f:
            content_string = f.read(MAX_CHARS)
            if is_truncated:
                return content_string + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content_string
    except Exception as e:
        raise Exception(f"Error: {e}")    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints the first 10,000 characters (truncated if necessary) of content in the specified file. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The target file given in relative path. Assume information given is in proper format."
            )
        }
    )
)         