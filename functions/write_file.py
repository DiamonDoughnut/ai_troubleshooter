from pathlib import Path

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