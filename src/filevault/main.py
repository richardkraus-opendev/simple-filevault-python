from crypto.aes import AESGCM
from file_manager import read_file, write_file
from cli import parse_args
from pathlib import Path
import os
import logging


def main() -> None:
    """
    main
    """

    aes = AESGCM()
    setup_logger()
    args = parse_args()
    input_file = Path(args.file)

    if not input_file.exists():
        logging.error(f"Input file does not exist: {input_file}")
        return 1
    
    output_path = get_output_path(args, input_file)
    if output_path.exists():
        logging.warning(f"Output file already exists and will be overwritten: {output_path}")
    
    if output_path.resolve() == input_file.resolve():
        logging.warning(
            "Output file cannot be the same as input file, overwriting original"
        )

    if args.command == "encrypt":
            
        data = read_file(input_file)

        logging.info(f"Encrypting {input_file} file and writing as {output_path}")
        encrypted = aes.encrypt(data, args.password)

        write_file(output_path, encrypted)

        logging.info("Encryption completed successfully")


    elif args.command == "decrypt":
        try:            
            data = read_file(input_file)

            logging.info(f"Decrypting {input_file} and writing as {output_path}")
            decrypted = aes.decrypt(data, args.password)

            write_file(output_path, decrypted)

            logging.info("Decryption completed successfully")
            
        except ValueError as e:
            logging.exception("Decryption failed")
            return 1 
    
    return 0


def setup_logger() -> None:
    """
    Configures application logging
    Logs are written both to console and to logs (app.log)
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

def get_output_path(args, input_file: Path) -> Path:
    """
    returns working output_path
    """

    if args.output:
        return Path(args.output)
    
    if args.command == "encrypt":
        return input_file.with_suffix(input_file.suffix + ".enc")

    if args.command == "decrypt":
        if input_file.suffix == ".enc":
            return input_file.with_suffix("")
        else:
            return Path(str(input_file) + ".dec")



if __name__ == "__main__":
    import sys
    sys.exit(main())