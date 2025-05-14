# imports
import os
import sys
import logging
from algorithm2 import analyse_words, process_words

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def main():
    wordlist_dir = f"{os.path.dirname(os.path.abspath(__file__))}\wordlists"
    filenames = [
        f"{wordlist_dir}\wordlist-5.7k.txt",
        f"{wordlist_dir}\wordlist-5.7k-guessable.txt",
    ]
    for filename in filenames:
        with open(
            filename, "r"
        ) as file_handle:  # open the wordlist and load it into a list
            words = file_handle.read().splitlines()
        words.sort()

        analyse_words(words)

        out_bytes = process_words(words)

        with open(f"{'.'.join(filename.split('.')[:-1])}.bin", "wb") as out_file:
            out_file.write(out_bytes)
        out_file.close()

        orig_filesize = os.path.getsize(filename)
        new_filesize = os.path.getsize(".".join(filename.split(".")[:-1]) + ".bin")
        log.info(
            f"file size of {'.'.join(filename.split('.')[:-1])}.bin is {new_filesize} bytes - {int((new_filesize/orig_filesize)*100)}% of original size"
        )


if __name__ == "__main__":
    main()
