# imports
import os

# Rules
# FIRST BYTE
# 1 for new word
# 2 bits for repeat of the first 0-3 of previous word
# 5 bits for letter
# 	0-25 is A-Z
# 	26 is ES
# 	27 is ER
# 	28 is ED
# 	29 is RE
# 	30 is IN
# 	31 is AR
#
# 0 for continued word
# 5 bits at a time for letter
#   0-25 is A-Z
#   26 is ES
#   27 is ER
#   28 is ED
#   29 is RE
#   30 is IN
#   31 is AR

# Example
#'aargh' - 10000000 01111100 01100011 01000000
#'abaca' - 10100001 00000000 00100000 00000000
#'abaci' - 11100010 00010000
#'abbey' - 11000001 00010011 00000000
#'ahead' - 10100111 00010000 00110000

def double_lookup(this_double):
    lookup={"es": 26,
            "er": 27,
            "ed": 28,
            "re": 29,
            "in": 30,
            "ar": 31}    
    if this_double in lookup:
        return(lookup[this_double],True)
    else:
        return(None,False)
    
def letter_to_bits(this_letter,next_letter):
    double_num,found=double_lookup(this_letter+next_letter)
    if found:
        return format(double_num,"05b"),1
    else:
        return format(ord(this_letter)-97,"05b"),0
    
def main():
    with open("wordlist\wordlist.txt","r") as file_handle:     # open the wordlist and load it into a list
        words = file_handle.read().splitlines()
    words.sort()
    out_bytes=bytearray()
    last_word=['x','x','x','x','x']
    for [*this_word] in words:
        word_bytes=bytearray()
        first_byte="1"      # First byte of a new word always starts with 1
        # Go through the repeated characters
        if this_word[:3]==last_word[:3]: # first three characters match
            first_byte=first_byte+"11"
            letter_bits,extra=letter_to_bits(this_word[3],this_word[4])
            first_byte=first_byte+letter_bits
            next_letter=4+extra #if the double letter hits, even better
        else:
            if this_word[:2]==last_word[:2]: # first two characters match
                first_byte=first_byte+"10"
                letter_bits,extra=letter_to_bits(this_word[2],this_word[3])
                first_byte=first_byte+letter_bits
                next_letter=3+extra
            else:
                if this_word[:1]==last_word[:1]: # first character matches
                    first_byte=first_byte+"01"
                    letter_bits,extra=letter_to_bits(this_word[1],this_word[2])
                    first_byte=first_byte+letter_bits
                    next_letter=2+extra
                else:
                    first_byte=first_byte+"00" # entirely new word
                    letter_bits,extra=letter_to_bits(this_word[0],this_word[1])
                    first_byte=first_byte+letter_bits
                    next_letter=1+extra

        print("first byte of %s is %s" % (this_word, first_byte))
        last_word=this_word
        out_bytes.append(int(first_byte,2))
        # The rest of the letters come next (it might not be necessary in very minor cases)
        
    print(out_bytes)

if __name__ == "__main__":
    main()
