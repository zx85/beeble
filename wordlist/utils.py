def double_lookup(this_double):
    lookup = {"ed": 28, "es": 27}
    if this_double in lookup:
        return lookup[this_double]
    else:
        return None


def letter_to_bits(chars):
    if double_num := double_lookup(chars):
        return format(double_num, "05b"), 1
    else:
        return format(ord(chars[0]) - 98, "05b"), 0
