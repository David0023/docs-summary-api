import uuid
import os

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def save_file(content: bytes) -> str:
    filepath = f"uploads/{uuid.uuid4()}"
    with open(filepath, "wb") as file:
        file.write(content)
    return filepath


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()