from pathlib import Path

def read_file(path: str) -> bytes:                  #reads file and returns its bytes
    file_path = Path(path)

    if (not file_path.exists()):                    #if file doesn't exists
        raise FileNotFoundError(f"File {path} not found.")  
    
    return file_path.read_bytes()

def write_file(path: str, data: bytes) -> none:     #writes bytes to a file
    file_path = Path(path)

    file_path.write_bytes(data)

