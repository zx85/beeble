# imports
import os
import logging
from utils import letter_to_bits

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


"""
Word analysis
index at start
qty of words starting with this letter
number of bytes containing words with this letter

"""


def analyse_words(words):
    initials = []
    analysis = {
        "second_letter_repeated": 0,
        "third_letter_repeated": 0,
        "fourth_letter_repeated": 0,
    }
    prev_word = "xxxxx"
    total_word_count = 0
    word_count = 0
    letter_pairs = {}
    for word in words:
        word_stub = word[1:5]
        if prev_word != "xxxxx" and word[0] != prev_word[0]:
            initials.append({"initial": prev_word[0], "qty": word_count})
            word_count = 0
        if word[1] == prev_word[1]:
            log.debug(f"previous second letter matches: {prev_word} | {word}")
            analysis["second_letter_repeated"] += 1
            word_stub = word[2:5]
        if word[1:3] == prev_word[1:3]:
            log.debug(f"previous second+third letters match: {prev_word} | {word}")
            analysis["third_letter_repeated"] += 1
            word_stub = word[3:5]
        if word[1:4] == prev_word[1:4]:
            log.debug(
                f"previous second+third+fourth letters match: {prev_word} | {word}"
            )
            analysis["fourth_letter_repeated"] += 1
            word_stub = word[4]
        if len(word_stub) > 1:
            for each_pair in range(len(word_stub) - 1):
                letter_pair = word_stub[each_pair : each_pair + 2]
                if letter_pair not in letter_pairs:
                    letter_pairs[letter_pair] = 1
                else:
                    letter_pairs[letter_pair] += 1
        word_count += 1
        total_word_count += 1
        prev_word = word
    # don't forget the z
    initials.append({"initial": word[0], "qty": word_count})
    for initial in initials:
        log.info(f"{initial}")
    log.info(f"Total word count: {total_word_count}")
    log.info(f"repeated words: {analysis}")
    sorted_letter_pairs = sorted(
        letter_pairs.items(), key=lambda item: item[1], reverse=True
    )

    for key, value in sorted_letter_pairs[:10]:
        log.debug(f"{key}: {value}")


"""
Process the words into a bytearray using the following rules:
    5 bits per letter
    31 = new word - second, third and fourth letters of previous words repeated
    30 = new word - second and third letters of previous word repeated
    29 = new word - second letter of previous word repeated
    28 = new word - no letters of previous word repeated
    27 = ed
    26 = es
    25-0 = letter of the alphabet (-1)
    
Algorithm for decoding:
    AND with 11100 to determine new word
    OR with 00011 to determine number of repeated letters

"""


def process_words(words):
    byte_array = bytearray()
    prev_word = ""
    prev_initial = ""
    initial_index = []
    for word in words:
        initial = word[0]
        # first 5 bits
        bit_string = "11100"
        start_char = 1
        if prev_word != "":
            # characters 2,3, and 4 match:
            if word[1:4] == prev_word[1:4]:
                bit_string = "11111"
                start_char = 4
            # characters 2 and 3 match:
            elif word[1:3] == prev_word[1:3]:
                bit_string = "11110"
                start_char = 3
            # character 2 matches
            elif word[1:2] == prev_word[1:2]:
                bit_string = "11101"
                start_char = 2
        skip = 0
        for chars in word[start_char : start_char + 2]:
            if skip == 0:
                bit_string, skip = letter_to_bits(chars)
        log.debug(f"Bit string for {word} is: {bit_string}")

        # prepare to go round the loop again
        prev_word = word
        if initial != prev_initial:
            initial_index.append({"initial": initial, "index": len(byte_array)})
        prev_initial = initial

        # create the new byte array prefixed with the initial index
        full_byte_array = byte_array

        return full_byte_array
