from utils import letter_to_bits
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

"""
# Algorithm 1
    This won't work because it's impossible to do lookups on the guessable word list this way.
    so I gave up.
    
    Rules
    FIRST BYTE
    1 bit (MSB) for new word
    2 bits for repeat of the first 0-3 of previous word
    5 bits for letter
        0-25 is A-Z
        26 is ES
        27 is ER
        28 is ED
        29 is RE
        30 is IN
        31 is AR

    0 (MSB) for continued word
    5 bits at a time for letter
    0-25 is A-Z
    26 is ES
    27 is ER
    28 is ED
    29 is RE
    30 is IN
    31 is AR

    Example
    'aargh' - 10000000 01111100 01100011 01000000
    'abaca' - 10100001 00000000 00100000 00000000
    'abaci' - 11100010 00010000
    'abbey' - 11000001 00010011 00000000
    'ahead' - 10100111 00010000 00110000
"""


def process_words(words):
    out_bytes = bytearray()
    prev_word = ["x", "x", "x", "x", "x"]
    for [*this_word] in words:
        first_byte = "1"  # First byte of a new word always starts with 1
        # First complete byte comprises 3 bits for lookup and the 5 bits for the first letter
        if this_word[:3] == prev_word[:3]:  # first three characters match
            first_byte = first_byte + "11"
            letter_bits, letter_skip = letter_to_bits(this_word[3], this_word[4])
            first_byte = first_byte + letter_bits
            next_letter = 4 + letter_skip  # if the double letter hits, even better
        else:
            if this_word[:2] == prev_word[:2]:  # first two characters match
                first_byte = first_byte + "10"
                letter_bits, letter_skip = letter_to_bits(this_word[2], this_word[3])
                first_byte = first_byte + letter_bits
                next_letter = 3 + letter_skip
            else:
                if this_word[:1] == prev_word[:1]:  # first character matches
                    first_byte = first_byte + "01"
                    letter_bits, letter_skip = letter_to_bits(
                        this_word[1], this_word[2]
                    )
                    first_byte = first_byte + letter_bits
                    next_letter = 2 + letter_skip
                else:
                    first_byte = first_byte + "00"  # entirely new word
                    letter_bits, letter_skip = letter_to_bits(
                        this_word[0], this_word[1]
                    )
                    first_byte = first_byte + letter_bits
                    next_letter = 1 + letter_skip

        print("first byte of %s is %s" % (this_word, first_byte))
        prev_word = this_word
        out_bytes.append(int(first_byte, 2))

        # The rest of the letters come next (it might not be necessary in very minor cases)
        cur_byte = ""
        for char in this_word[next_letter:]:
            if cur_byte == "":
                # first byte of a continued word always starts with 0
                cur_byte = "0"
            letter_bits, letter_skip = letter_to_bits(char, "x")

            if letter_skip:
                break
    return out_bytes
