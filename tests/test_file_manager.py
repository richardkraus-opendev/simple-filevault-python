import pytest
from filevault.file_manager import read_file, write_file

def test_successful_write_and_read(tmp_path):

    test_file = tmp_path / "test.txt"

    data = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit."

    write_file(test_file, data)

    read_from_file = read_file(test_file)

    assert read_from_file == data

def test_successful_folder_creation(tmp_path):

    nested_file = tmp_path / "new_dir" / "subdir" / "test.txt"

    data = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit."

    write_file(nested_file, data)

    assert nested_file.exists()

def test_nonexisting_file(tmp_path):

    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        read_file(missing_file)

