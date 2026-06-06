import logging
from pathlib import Path

def read_file(path: Path) -> bytes:
    """
    reads file and returns its bytes
    """ 
    try:
        return path.read_bytes()
    except Exception as e:
        logging.exception(f"Failed to read file: {path}")
        raise

def write_file(path: Path, data: bytes) -> None:
    """
    writes bytes to the file, creating parent directories if needed
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    except Exception as e:
        logging.exception(f"Failed to write file: {path}")
        raise

