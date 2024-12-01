#!/usr/bin/env python

from __future__ import annotations

"""
Represent file system as a dict of directories.  Track the size
of directories which is None on first scan, then calculated after
the directory structure is mapped out.

Making some hard assumptions based on the input:
- only cd to / once on the first line
- every other cd is to a subdirectory or a parent
"""

import fileinput

from dataclasses import dataclass

DISK_SIZE = 70000000
FREE_SPACE_NEEDED = 30000000

@dataclass
class File:
    name: str
    size: int

@dataclass
class Directory:
    path: str
    parent: Directory
    subdirectories: list[Directory]
    files: list[File]
    size: int 

lines = [line.strip() for line in fileinput.input()]

directories: dict[str, Directory] = {}

# hard code root directory so that loop can assume any "non-.. cd" is to a 
# sub-directory of the current directory
root_directory = Directory("/", None, [], [], None)
current_directory = root_directory
directories = {
    "/": root_directory
}

for line in lines[1:]:
    """
    all lines start with:
      - $ cd <directory_name>: go to a subdirectory 
      - $ cd ..: go to parent
      - $ ls: do nothing
      - anything else: we are in an `ls` block and see a directory/file
    """

    if line.startswith('$ cd ..'):
        current_directory = directories[current_directory.path].parent
        continue

    if line.startswith('$ cd'):
        directory_name = line.split()[2]
        current_directory = directories[f"{current_directory.path}{directory_name}/"]
        continue

    if line.startswith('$ ls'):
        continue

    # else we are seeing a file/subdirectory
    if line.startswith('dir'):
        directory_name = line.split()[1]
        directory_path = f"{current_directory.path}{directory_name}/"
        directory = Directory(directory_path, current_directory, [], [], None)
        directories[directory_path] = directory
        current_directory.subdirectories.append(directory)
    else:
        file_size, file_name = line.split()
        file = File(file_name, int(file_size))
        current_directory.files.append(file)

def directory_size(directory: Directory) -> int:
    """
    Get a directory size, calculating it recursively if needed
    """
    if directory.size is not None:
        return directory.size

    size = 0
    for subdirectory in directory.subdirectories:
        size += directory_size(subdirectory)

    for file in directory.files:
        size += file.size

    directory.size = size
    return size

total_storage = directory_size(root_directory)

sum_size_of_directories_under_100k = 0
sizes_removable_to_free_up_enough_space = []

for directory in directories.values():
    print(f"{directory.path}: {directory.size}")

    if directory.size < 100000:
        sum_size_of_directories_under_100k += directory.size

    if DISK_SIZE - total_storage + directory.size >= FREE_SPACE_NEEDED:
        sizes_removable_to_free_up_enough_space.append(directory.size)

print()
print(f"part one: {sum_size_of_directories_under_100k}")
print(f"part two: {min(sizes_removable_to_free_up_enough_space)}")
