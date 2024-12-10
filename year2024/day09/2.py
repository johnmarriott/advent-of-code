#!/usr/bin/env python

"""
Store the files and free spaces in dictionaries.  Files will be looked up by id and free spaces
by index, so these are the keys of their dicts.  Then to make a swap, put the file in the lowest-indexed
free space that can hold it, and recalculate free spaces.

Calling this "files/spaces" representation "data" and "memory" is when it's a combined array.
"""

from dataclasses import dataclass
import fileinput

FREE_SPACE = '.'

@dataclass
class File:
    index: int
    length: int
    id: int

@dataclass
class FreeSpace:
    index: int
    length: int

def input_to_data(input) -> tuple[dict[int, File], dict[int, FreeSpace]]:
    files = {}
    free_spaces = {}

    character_is_file_length = True # toggles on each character read
    files_parsed = 0
    next_index = 0

    for character in input:
        data_length = int(character)
        if character_is_file_length:
            files[files_parsed] = File(
                next_index, 
                data_length,
                files_parsed
            )
            files_parsed += 1

        else:
            free_spaces[next_index] = FreeSpace(
                next_index, 
                data_length
            )

        next_index += data_length
        character_is_file_length = not character_is_file_length

    return files, free_spaces

def data_to_memory(files: dict[int, File], free_space: dict[int, FreeSpace]) -> list:
    files_by_index = {file.index: file for file in files.values()}

    max_index = max(
        max([file.index + file.length for file in files.values()]),
        max([free_space.index + free_space.length for free_space in free_space.values()])
    )

    memory = []

    for i in range(max_index):
        if i in files_by_index:
            for j in range(files_by_index[i].length):
                memory.append(files_by_index[i].id)
        elif i in free_space:
            for j in range(free_space[i].length):
                memory.append(FREE_SPACE)

    return memory

def print_memory(files: dict[int, File], free_spaces: dict[int, FreeSpace]):
    memory = data_to_memory(files, free_spaces)
    for cell in memory:
        print(cell, end='')
    print()

def memory_checksum(memory) -> int:
    checksum = 0

    for i in range(len(memory)):
        if memory[i] == FREE_SPACE:
            continue

        checksum += i * memory[i]

    return checksum

def combine_contiguous_free_spaces(free_spaces: dict[int, FreeSpace]):
    # thought this might be necessary
    # but it wasn't for this puzzle's input 🤷
    return

def defrag_memory(files: dict[int, File], free_spaces: dict[int, FreeSpace]) -> list[str]:
    file_ids = list(reversed(sorted(files.keys())))

    for file_id in file_ids:
        file = files[file_id]

        available_free_memory_indices = [
            free_space.index
            for free_space in free_spaces.values()
            if free_space.length >= file.length
        ]

        if not available_free_memory_indices:
            # cannot move this file
            continue

        memory_index = min(available_free_memory_indices)

        if memory_index < file.index:
            move_file(files, free_spaces, memory_index, file.id)

        combine_contiguous_free_spaces(free_spaces)

    memory = data_to_memory(files, free_spaces)
    return memory

def move_file(
        files: dict[int, File], 
        free_spaces: dict[int, FreeSpace], 
        index: int, 
        file_id: int
    ):

    file = files[file_id]
    file_length = files[file_id].length
    free_space = free_spaces[index]

    if free_space.length > file_length:
        free_spaces[index + file_length] = FreeSpace(
            index + file_length,
            free_space.length - file_length
        )

    del free_spaces[index]

    free_spaces[file.index] = FreeSpace(
        file.index,
        file.length
    )

    file.index = index


input = [line.strip() for line in fileinput.input()][0]

files, free_space = input_to_data(input)
memory = defrag_memory(files, free_space)

print(memory_checksum(memory))
