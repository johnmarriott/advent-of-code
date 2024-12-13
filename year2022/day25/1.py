#!/usr/bin/env python

import fileinput
import math

snafu_character_to_number = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

snafu_number_to_character = {
    2: "2",
    1: "1",
    0: "0",
    -1: "-",
    -2: "=",
}

def snafu_to_decimal(snafu: str) -> int:
    exponent = len(snafu)
    place_values = []

    for digit in snafu:
        exponent -= 1
        place_values.append(snafu_character_to_number[digit] * (5 ** exponent))

    return sum(place_values)

def decimal_to_snafu(decimal_value: int) -> str:
    """
    1. round the value up to the smallest "all twos" quinary number that can hold it,
       e.g., 50_d can fit in 222_q = 62_d, but not 22_q = 12_d
    2. start with the all-twos number, and find the regular quinary digits that make
       up the difference between the all-twos and the desired value
    3. subtract the difference (offset) digits from the all-twos number, and 
       translate these to snafu characters
    """

    n_snafu_upper_bound_digits = 1
    snafu_upper_bound = 2

    while decimal_value > snafu_upper_bound:
        n_snafu_upper_bound_digits += 1
        snafu_upper_bound += 2 * (5 ** (n_snafu_upper_bound_digits - 1))

    snafu_digits = [2] * n_snafu_upper_bound_digits

    # find offset digits that make up the value remaining,
    # will be subtracted (item-wise) from the snafu digits
    value_remaining = abs(decimal_value - snafu_upper_bound)
    offset_digits = []

    exponent = n_snafu_upper_bound_digits - 1
    while exponent >= 0:
        snafu_place_value = 5 ** exponent
        digit = math.floor(value_remaining / snafu_place_value)
        value_remaining -= digit * snafu_place_value
        offset_digits.append(digit)
        exponent -= 1

    for i in range(len(snafu_digits)):
        snafu_digits[i] -= offset_digits[i]

    snafu_characters = map(snafu_number_to_character.get, snafu_digits)
    return("".join(snafu_characters))


lines = [line.strip() for line in fileinput.input()]

decimal_values = []
for line in lines:
    decimal_values.append(snafu_to_decimal(line))

decimal_sum = sum(decimal_values)
print(decimal_to_snafu(decimal_sum))
