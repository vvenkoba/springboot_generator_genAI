from pathlib import Path

def write_generated_file(file_path: Path, content: str):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip())