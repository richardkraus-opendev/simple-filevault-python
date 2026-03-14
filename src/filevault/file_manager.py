from pathlib import Path

def read_file(path: Path) -> bytes:
    """
    reads file and returns its bytes
    """ 
    return path.read_bytes()

def write_file(path: Path, data: bytes) -> None:
    """
    writes bytes to the file
    """
    path.write_bytes(data)

