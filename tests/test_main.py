import pytest
import argparse
from pathlib import Path
from filevault.main import get_output_path
from filevault.main import main
from filevault.crypto.aes import AESGCM

@pytest.mark.parametrize("command, input_name, output_arg, expected_name", [
    ("encrypt", "test.txt", None, "test.txt.enc"),
    ("encrypt", "test.txt", "custom.enc", "custom.enc"),
    ("decrypt", "test.txt.enc", None, "test.txt"),
    ("decrypt", "data.bin", None, "data.bin.dec"),
])

def test_successful_get_output_path(command, input_name, output_arg, expected_name):

    args = argparse.Namespace(command=command, output=output_arg)

    input_file = Path(input_name)

    result = get_output_path(args, input_file)

    assert result == Path(expected_name)

def test_main_encrypt_success(tmp_path, mocker):

    args = argparse.Namespace(
        command="encrypt",
        file=str(tmp_path / "text.txt"),
        password="Password1234",
        output=None
    )
    mocker.patch("filevault.main.parse_args", return_value=args)

    mocker.patch("filevault.main.setup_logger")

    input_file = tmp_path / "text.txt"
    input_file.write_bytes(b"Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    result = main()

    assert result == 0

    expected_output = tmp_path / "text.txt.enc"

    assert expected_output.exists()

    encrypted_content = expected_output.read_bytes()
    assert encrypted_content.startswith(b'FILEVAULT\x00')

def test_main_decrypt_success(tmp_path, mocker):

    args = argparse.Namespace(
        command="decrypt",
        file=str(tmp_path / "text.txt.enc"),
        password="Password1234",
        output=None
    )
    mocker.patch("filevault.main.parse_args", return_value=args)

    mocker.patch("filevault.main.setup_logger")

    aes = AESGCM()
    input_file = tmp_path / "text.txt.enc"
    input_file.write_bytes(aes.encrypt(b"Lorem ipsum dolor sit amet, consectetur adipiscing elit.", "Password1234"))

    result = main()

    assert result == 0

    expected_output = tmp_path / "text.txt"

    assert expected_output.exists()

    decrypted_content = expected_output.read_bytes()
    assert decrypted_content == b"Lorem ipsum dolor sit amet, consectetur adipiscing elit."


def test_main_non_existing_file(tmp_path, mocker):

    args = argparse.Namespace(
        command="encrypt",
        file=str(tmp_path / "non_existing_file"),
        password="Password1234",
        output=None
    )
    mocker.patch("filevault.main.parse_args", return_value=args)

    mocker.patch("filevault.main.setup_logger")

    result = main()

    assert result == 1

    expected_output = tmp_path / "non_existing_file"

    assert not expected_output.exists()


