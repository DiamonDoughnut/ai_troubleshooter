import os
import sys
from pathlib import Path

def get_files_info(working_directory, directory="."):
    try:
        working_dir = Path(working_directory).resolve()
        target_dir = (working_dir / directory).resolve()

        if not target_dir.is_relative_to(working_dir):
            raise ValueError(f"Error: Cannot list {directory} as it is outside the permitted working directory")
        if not target_dir.is_dir():
            raise ValueError(f"Error: {directory} is not a directory")

        results = []
        for item in target_dir.iterdir():
            name = item.name
            is_dir = item.is_dir()
            if item.is_file():
                size = item.stat().st_size
            if item.is_dir():
                size = get_dir_size(item)
            results.append(f" - {name}: file_size={size} bytes, is_dir={is_dir}")   
        return results             
    except Exception as e:
        raise Exception(f"Error: {e}")


def get_dir_size(path_obj):
    total_size = 0
    try:
        for item in path.iterdir():
            if item.is_file():
                total_size += item.stat().st_size
            if item.is_dir():
                total_size += get_dir_size(item)
    except:
        pass
    return total_size                    