from pathlib import Path

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