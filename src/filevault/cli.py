import argparse

def parse_args():
    """
    Parses arguments from user
    """

    parser = argparse.ArgumentParser(
        description="Simple tool for file encryption and decryption\n"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    encrypt_parser = subparsers.add_parser(
        "encrypt",
        help="Encrypt a file"
    )
    encrypt_parser.add_argument(
        "--file", "-f",
        required=True,
        help="Input file to encrypt"
    )
    encrypt_parser.add_argument(
        "--output","-o",
        required=False,
        help="Output file path, if not provided, default extension will be used (.enc)"
    )
    encrypt_parser.add_argument(
        "--password", "-p",
        required=True,
        help="Password used for encryption"
    )

    decrypt_parser = subparsers.add_parser(
        "decrypt",
        help="Decrypt a file"
    )
    decrypt_parser.add_argument(
        "--file", "-f",
        required=True,
        help="Encrypted file"
    )
    decrypt_parser.add_argument(
        "--output","-o",
        required=False,
        help="Output file path, if not provided, default extension will be used (.dec) or original name (pre encryption)"
    )
    decrypt_parser.add_argument(
        "--password", "-p",
        required=True,
        help="Password used for decryption"
    )

    return parser.parse_args()

