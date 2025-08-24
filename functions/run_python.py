from pathlib import Path
import sys
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    working_dir = Path(working_directory).resolve()
    target_file = (working_dir / file_path).resolve()

    if not target_file.is_relative_to(working_dir):
        raise ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not target_file.is_file():
        raise ValueError(f'Error: File "{file_path}" not found')
    if not target_file.suffix == ".py":
        raise ValueError(f'Error: "{file_path}" is not a Python file.')   

    command = [
        str(sys.executable),
        str(target_file)
    ]     

    if args:
        command.extend(args)

    try:
        result_str = ""

        result_obj = subprocess.run(
            command,
            cwd=working_dir,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )

        if result_obj.stdout:
            result_str += f"STDOUT:\n{result_obj.stdout}"

        if result_obj.stderr:
            result_str += f"\n\n\nSTDERR:\n{result_obj.stderr}"    

        if result_obj.returncode != 0:
            result_str += f"\n\n\nProcess exited with code {e.returncode}"

        if result_str == "":
            result_str += "No output produced."
        return result_str

    except Exception as e:
        raise Exception(f"Error: executing Python file: {e}")        
