#!/usr/bin/env python

"""
big idea for part two:

Worked out on paper what the values of the registers and the output would be after
one cycle through the program (made easier since the second-last instruction is an
output and the last instruction is a jump to restart if A ≠ 0).  (One cycle is one
pass through the instruction set, not including a restart.)

Denoting A,B,C as the values of those registers at the start of one cycle and
A', B', C' as the values at the end, then A' = floor(A / 8) and B', C', and the
cycle's output are expressed in terms of A.

Therefore a solution that produces a tail of the desired output still produces
that tail if it's bit-shifted left by 3, regardless of the lower three bits:
only the initial value of A matters, and it gets bit-shifted right in the cycle.
Also, the number of digits in the output is log base 8 of the initial value of A.

For example, in my input 1536 produces [3, 5, 3, 0].  All of the values
1536 * 8 + {0, 1, 2, 3, 4, 5, 6, 7} yield some [x, 3, 5, 3, 0].  These
eight can be tested to see which one has right value.

Use this process to construct the full solution, from the end of the required
output to the start.
"""

from dataclasses import dataclass
from enum import IntEnum
import fileinput

@dataclass
class Program:
    a: int
    b: int
    c: int
    instructions: list[int]

class Instruction(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

def parse_input(lines: list[str]) -> Program:
    for line in lines:
        if line.startswith('Register A'):
            a = int(line.split(':')[1].strip())

        if line.startswith('Register B'):
            b = int(line.split(':')[1].strip())

        if line.startswith('Register C'):
            c = int(line.split(':')[1].strip())

        if line.startswith('Program'):
            instructions = list(map(int, line.split(':')[1].strip().split(',')))

    return Program(a, b, c, instructions)

def execute_instruction(program: Program, instruction_pointer: int) -> tuple[int, int]:
    instruction = program.instructions[instruction_pointer]
    operand = program.instructions[instruction_pointer + 1]
    output = None
    
    if instruction != Instruction.JNZ: 
        # for all other instructions, the pointer advances by 2
        instruction_pointer += 2

    combo_operand = operand
    if operand == 4:
        combo_operand = program.a
    elif operand == 5:
        combo_operand = program.b
    elif operand == 6:
        combo_operand = program.c

    if instruction == Instruction.ADV:
        program.a = program.a // 2**combo_operand
    elif instruction == Instruction.BXL:
        program.b = program.b ^ operand
    elif instruction == Instruction.BST:
        program.b = combo_operand % 8
    elif instruction == Instruction.JNZ:
        if program.a != 0:
            instruction_pointer = operand
        else:
            instruction_pointer += 2
    elif instruction == Instruction.BXC:
        program.b = program.b ^ program.c
    elif instruction == Instruction.OUT:
        output = combo_operand % 8
    elif instruction == Instruction.BDV:
        program.b = program.a // 2**combo_operand
    elif instruction == Instruction.CDV:
        program.c = program.a // 2**combo_operand

    return instruction_pointer, output

def run_program(program: Program) -> list[int]:
    instruction_pointer = 0
    output = []

    while instruction_pointer < len(program.instructions):
        instruction_pointer, out = execute_instruction(program, instruction_pointer)
        if out is not None:
            output.append(out)

    return output
        
lines = [line.strip() for line in fileinput.input()]
program = parse_input(lines)

## part two
# do this first so that the program's registers are fresh when
# they're copied to test programs

candidate_a_values = [0]
for i in range(len(program.instructions) - 1, -1, -1):
    # match the output from end to start
    output_to_match = program.instructions[i:]
    next_candidate_a_values = []

    for candidate_a_value in candidate_a_values:
        for d in range(8):
            test_a = candidate_a_value * 8 + d
            test_program = Program(test_a, program.b, program.c, program.instructions)
            output = run_program(test_program)

            if output == output_to_match:
                next_candidate_a_values.append(test_a)

    candidate_a_values = next_candidate_a_values

## part one
# do this second since it will modify `program` in place

output = run_program(program)

print(f'part one: {",".join(map(str, output))}')
print(f"part two: {min(candidate_a_values)}")
