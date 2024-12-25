#!/usr/bin/env python

"""
Problem says that the machine should be an adder.  Inspecting the connections, 
this is a 45-bit adder: the x00 and y00 inputs go into a half-adder, which yields
a carry bit to the full adders that x01 and y01 feed into, and so on.  The final
carry bit is the last bit of the sum.

Find the misplaced gates by checking where the properties of the correct adder machine
are violated:

- all x/y-inputs should go into one XOR and one AND each (no violations of this)
- no z-wire should be an input to any gate (no violations of this)
- any gate with a z-output should be an XOR
- all inputs to OR gates should be an output of an AND gate.  This will
  yield a false positive in the first half adder
- conversely, all outputs of AND gates should be inputs to OR gates
- all "middle" gates, that don't have an x/y-input nor a z-output, should 
  be only AND and OR gates (no XOR gates)

Checking these, we find ten swappable outputs, but two of them are the two 
false positives noted above.
"""


from dataclasses import dataclass
from itertools import permutations, combinations
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


def parse_input(lines) -> tuple[dict[str, bool], list[Gate]]:
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


def wire_letter_value(letter: str, wires: dict[str, bool]) -> int:
    """
    Returns the number constructed by the wires that start with the given letter.
    For example, if the set of wires contains z00, x00, and z01, then 
    wire_letter_value("z", wires) will return the number with binary digits
    z01z00
    """
    output = 0

    for name, value in wires.items():
        if name.startswith(letter):
            exponent = int(name[1:])
            output += int(value) * 2 ** exponent

    return output


def run_circuit(wires: dict[str, bool], gates: list[Gate]) -> dict[str, bool]:
    all_wires_known = False
    passes = 0
    while not all_wires_known and passes < 1000:
        for gate in gates:
            gate.execute(wires)

        all_wires_known = all(wire is not None for wire in wires.values())
        passes += 1

    if passes == 1000:
        # in case it's been swapped into a malformed machine
        return None

    return wires


def swap_outputs(gates: list[Gate], wire_a: str, wire_b: str):
    for gate in gates:
        if gate.wire_out == wire_a:
            gate.wire_out = wire_b
        elif gate.wire_out == wire_b:
            gate.wire_out = wire_a


def machine_swappable_outputs(gates: list[Gate]) -> set[str]:
    """
    Returns a set of all wire outputs that can be swapped without changing the
    output of the circuit.
    """
    swappable_outputs = set()

    # flag anything going into a z-output that's not an XOR gate
    for gate in gates:
        if (
            gate.wire_out.startswith("z") 
            and gate.type != "XOR"
        ):
            swappable_outputs.add(gate.wire_out)

    # check that all inputs to OR gates are preceded by AND gates
    inputs_to_or = set()
    for gate in gates:
        if gate.type == "OR":
            inputs_to_or.add(gate.wire_a)
            inputs_to_or.add(gate.wire_b)

    for gate in gates:
        if gate.wire_out in inputs_to_or:
            if gate.type != "AND":
                swappable_outputs.add(gate.wire_out)

    # check that all AND gates feed into OR gates
    and_outputs = [gate.wire_out for gate in gates if gate.type == "AND"]
    for and_output in and_outputs:
        if and_output not in inputs_to_or:
            swappable_outputs.add(and_output)

    # check that all gates that don't have an x/y-input nor a z-output
    # are not XOR gates
    for gate in gates:
        if (
            not gate.wire_a.startswith("x")
            and not gate.wire_b.startswith("x")
            and not gate.wire_a.startswith("y")
            and not gate.wire_b.startswith("y")
            and not gate.wire_out.startswith("z")
        ):
            if gate.type == "XOR":
                swappable_outputs.add(gate.wire_out)

    return swappable_outputs


def try_swapping_wires(swappable_wires: set[str], wires: dict[str, bool], gates: list[Gate]) -> tuple[str]:
    wire_permutations = list(permutations(swappable_wires, 8))

    for i, wire_output_swaps in enumerate(wire_permutations):
        four_swaps = [
            (wire_output_swaps[0], wire_output_swaps[1]),
            (wire_output_swaps[2], wire_output_swaps[3]),
            (wire_output_swaps[4], wire_output_swaps[5]),
            (wire_output_swaps[6], wire_output_swaps[7]),
        ]

        # swap these outputs
        for wire_a, wire_b in four_swaps:
            for gate in gates:
                if gate.wire_out == wire_a:
                    gate.wire_out = wire_b
                elif gate.wire_out == wire_b:
                    gate.wire_out = wire_a

        # see if this does it
        output = run_circuit(wires, gates)

        if output is not None:
            x = wire_letter_value("x", output)
            y = wire_letter_value("y", output)
            z = wire_letter_value("z", output)

            if x + y == z:
                return wire_output_swaps

        # swap them back
        for wire_a, wire_b in four_swaps:
            for gate in gates:
                if gate.wire_out == wire_a:
                    gate.wire_out = wire_b
                elif gate.wire_out == wire_b:
                    gate.wire_out = wire_a

    return None


lines = [line.strip() for line in fileinput.input()]
wires, gates = parse_input(lines)
output_wires = set(gate.wire_out for gate in gates)

swappable_outputs = machine_swappable_outputs(gates)

# can manually remove these (they are the two false positives, the final output
# and the output of [x00 XOR y00]) for my problem's input
try:
    swappable_outputs.remove("z45")
    swappable_outputs.remove("gwq")
    print(",".join(sorted(swappable_outputs)))
except KeyError:
    # if running this on a different input, can just try all different 4-swaps
    # of the swappable outputs until it works
    wires_to_swap = try_swapping_wires(swappable_outputs, wires, gates)
    print(",".join(sorted(wires_to_swap)))
