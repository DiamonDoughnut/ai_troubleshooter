from pathlib import Path
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir = Path(working_directory).resolve()
        target_file = (working_dir / file_path).resolve()

        if not target_file.is_relative_to(working_dir):
            raise ValueError(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.touch()

        target_file.write_text(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        raise Exception(f"Error: {e}")    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites a file in the target directory. If the file does not exist, creates the files and any directories needed. Constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to which content will be written (including the file extension), relative to the working directory. Assume info given is proper format."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text to write to the created/targeted file. Will completely erase target file (or create completely blank file) if left blank. If not given, default to empty string."
            )
        }
    )
)         