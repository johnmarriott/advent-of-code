#!/usr/bin/env python

import fileinput

FREE_SPACE = '.'

def print_memory(memory):
    for i in range(len(memory)):
        print(memory[i], end='')
    print()

def memory_checksum(memory) -> int:
    checksum = 0
    for i in range(len(memory)):
        if memory[i] == FREE_SPACE:
            break

        checksum += i * memory[i]

    return checksum

input = [line.strip() for line in fileinput.input()][0]

memory = []

character_is_file_length = True # toggles on each character read
files_parsed = 0
for character in input:
    id_or_free_space = FREE_SPACE

    if character_is_file_length:
        id_or_free_space = files_parsed
        files_parsed += 1

    for _ in range(0, int(character)):
        memory.append(id_or_free_space)

    character_is_file_length = not character_is_file_length

memory_is_sorted = False
while not memory_is_sorted:
    first_free_space_index = memory.index(FREE_SPACE)
    last_file_index = max([i for i in range(len(memory)) if memory[i] != FREE_SPACE])

    # if the first free space is after the last file, the memory is sorted
    if first_free_space_index > last_file_index:
        memory_is_sorted = True
    else:
        # swap the file and free space
        memory[first_free_space_index], memory[last_file_index] = memory[last_file_index], memory[first_free_space_index]
 
print(memory_checksum(memory))
