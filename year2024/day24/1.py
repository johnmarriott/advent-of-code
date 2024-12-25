#!/usr/bin/env python

from dataclasses import dataclass
import fileinput


@dataclass
class Gate:
    type: str
    wire_a: str
    wire_b: str
    wire_out: str

    def execute(self, wires: dict[str, bool]):
        if wires[self.wire_a] is None or wires[self.wire_b] is None:
            return

        if self.type == "AND":
            wires[self.wire_out] = wires[self.wire_a] & wires[self.wire_b]
        elif self.type == "OR":
            wires[self.wire_out] = wires[self.wire_a] | wires[self.wire_b]
        elif self.type == "XOR":
            wires[self.wire_out] = wires[self.wire_a] ^ wires[self.wire_b]


def parse_input(lines: list[str]) -> tuple[dict[str, bool], list[Gate]]:
    wires = {}
    gates = []

    for line in lines:
        if ":" in line:
            wire_name, wire_value = line.split(":")
            wires[wire_name] = bool(int(wire_value))
        elif len(line) > 0:
            wire_a, gate_type, wire_b, _, wire_out = line.split(" ")
            gates.append(Gate(gate_type, wire_a, wire_b, wire_out))

            if wire_out not in wires:
                wires[wire_out] = None

    return wires, gates


lines = [line.strip() for line in fileinput.input()]
wires, gates = parse_input(lines)

all_wires_known = False
while not all_wires_known:
    for gate in gates:
        gate.execute(wires)

    all_wires_known = all(wire is not None for wire in wires.values())

output = 0
for name, value in wires.items():
    if name.startswith("z"):
        exponent = int(name[1:])
        output += int(value) * 2 ** exponent

print(output)
