import uuid
import os

def save_file(content: bytes) -> str:
    filepath = f"uploads/{uuid.uuid4()}"
    with open(filepath, "wb") as file:
        file.write(content)
    return filepath


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def delete_file(filepath: str) -> None:
    if os.path.exists(filepath):
        os.remove(filepath)