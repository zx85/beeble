# imports
import os


# Quick utility file to extract the guessable (but not used for the puzzle) words from the full word list
def main():
    with open(
        "wordlist\wordlist-5.7k.txt", "r"
    ) as file_handle:  # open the wordlist and load it into a list
        words = file_handle.read().splitlines()
    words.sort()

    with open("wordlist\wordlist-full.txt", "r") as all_words_file:
        all_words = all_words_file.read().splitlines()
    all_words.sort()

    with open("wordlist\wordlist-5.7k-guessable.txt", "w") as out_file:
        for word in all_words:
            if word not in words:
                out_file.write(word + "\n")
    out_file.close()


if __name__ == "__main__":
    main()
