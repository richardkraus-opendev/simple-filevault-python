from crypto_engine import get_keys_32, encrypt_AES, decrypt_AES
from file_manager import read_file, write_file
import os
import logging

def main() -> None:
    """
    main
    """

    setup_logger()

    input_file = "examples/sample.txt"
    encrypted_file = "examples/sample.txt.enc"
    decrypted_file = "examples/sample.txt.enc.dec"

    try:
        original_data = read_file(input_file)
        key = get_keys_32()

        logging.info(f"Encypting {input_file} file with AES key = [{key}] and writing as {encrypted_file}.")
        encrypted_data = encrypt_AES(original_data, key)
        write_file(encrypted_file, encrypted_data)

        logging.info(f"Decrypting {encrypted_file} and writing as {decrypted_file}.")
        encrypted_data_from_file = read_file(encrypted_file)
        decrypted_data = decrypt_AES(encrypted_data_from_file, key)
        write_file(decrypted_file, decrypted_data)

        logging.info("Process completed successfully.")
    except FileNotFoundError as e:
        logging.exception(f"File not found: {e.filename}.")
    except ValueError:
        logging.exception("Decryption failed (authentication error).")

def setup_logger() -> None:
    """
    Configures application logging.
    Logs are written both to console and to logs/app.log file.
    """

    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/app.log"),
            logging.StreamHandler()
        ]
    )



"""
main() runs only when this file is executed directly (not when it is imported as a module).
"""
if __name__ == "__main__":
    import sys
    sys.exit(main())