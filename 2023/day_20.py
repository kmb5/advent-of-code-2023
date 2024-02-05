from __future__ import annotations
from dataclasses import dataclass, field
from abc import ABC

sample = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

sample2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


@dataclass
class Module:
    name: str
    pulse: int = 0
    pulses_received: list[tuple[Module, int]] = field(default_factory=list)
    inputs: list[Module] = field(default_factory=list)
    outputs: list[Module] = field(default_factory=list)

    def get_pulse(self, source: Module, pulse: int):
        print(f"{source.name} -{pulse}-> {self.name}")
        self.pulses_received.append((source, pulse))

    def connect(self, destination: Module):
        if destination not in self.outputs:
            self.outputs.append(destination)
        if self not in destination.inputs:
            destination.inputs.append(self)

    def __str__(self):
        n = self.name.upper() if self.pulse == 1 else self.name
        return f"<<{n}>> IN:{len(self.inputs)} OUT:{len(self.outputs)}"

    def __repr__(self):
        return str(self)


@dataclass
class Broadcaster(Module):
    def process_pulse(self):
        for module, pulse in self.pulses_received:
            for output in self.outputs:
                # print(f"{self.name} -{pulse}-> {output.name}")
                output.get_pulse(self, pulse)
        self.pulses_received = []

    def __str__(self):
        n = self.name.upper() if self.pulse == 1 else self.name
        return f"<<{n}>> IN:{len(self.inputs)} OUT:{len(self.outputs)}"

    def __repr__(self):
        return str(self)


@dataclass
class FlipFlop(Module):
    def process_pulse(self):
        for module, pulse in self.pulses_received:
            if pulse == 0:
                self.pulse = 0 if self.pulse else 1

                for module in self.outputs:
                    module.get_pulse(self, self.pulse)
        self.pulses_received = []

    def __str__(self):
        n = self.name.upper() if self.pulse == 1 else self.name
        return f"<<{n}>> IN:{len(self.inputs)} OUT:{len(self.outputs)}"

    def __repr__(self):
        return str(self)


@dataclass
class Conjunction(Module):
    most_recent_received = {}

    def process_pulse(self):
        for module, pulse in self.pulses_received:
            self.most_recent_received[module.name] = pulse
            if set(self.most_recent_received.values()) == {1}:
                p = 0
            else:
                p = 1

            for output in self.outputs:
                output.get_pulse(self, p)

        self.pulses_received = []

    def __str__(self):
        n = self.name.upper() if self.pulse == 1 else self.name
        return f"<<{n}>> IN:{len(self.inputs)} OUT:{len(self.outputs)}"

    def __repr__(self):
        return str(self)


class Output(Module):
    def process_pulse(self):
        pass


def create_module(t: str) -> Module:
    if t == "broadcaster":
        return Broadcaster(t)
    elif t == "output":
        return Output(t)

    typ, name = t[0], t[1:]
    if typ == "%":
        return FlipFlop(name)
    if typ == "&":
        return Conjunction(name)
    raise AttributeError(f"invalid type {typ}")


def get_module(name: str, modules: list[Module]):
    for module in modules:
        if module.name == name:
            return module
    return None


def parse(inp) -> list[Module]:
    modules_dict = {}
    parsed_modules = []

    for row in inp.splitlines():
        module, destinations = row.split(" -> ")

        parsed_modules.append(create_module(module))
        if module in ("broadcaster", "output"):
            modules_dict[module] = destinations.split(", ")
        else:
            modules_dict[module[1:]] = destinations.split(", ")

    for destination in destinations.split(", "):
        try:
            pm = create_module(destination)
            if pm not in parsed_modules:
                parsed_modules.append(pm)
        except AttributeError:
            continue

    for mname, destinations in modules_dict.items():
        module = get_module(mname, parsed_modules)
        for destination in destinations:
            dmodule = get_module(destination, parsed_modules)
            module.connect(dmodule)

    return parsed_modules


def all_processed(modules: list[Module]):
    for module in modules:
        if module.pulses_received and module.name != "output":
            return False

    return True


def push_button(modules: list[Module]):
    button = Module("button")
    modules[0].get_pulse(button, 0)

    while not (all_processed(modules)):
        for module in modules:
            module.process_pulse()


def part1(inp):
    modules = parse(inp)
    print(modules)
    push_button(modules)


def part2(inp):
    pass


def main():
    with open(
        "/Users/mako/github/advent-of-code-2023/2023/inputs/day_20_input.txt",
        encoding="utf-8",
    ) as f:
        inp = f.read()

    part1_sol = part1(sample2)
    print("Part 1: ", part1_sol)

    part2_sol = part2(inp)
    print("Part 2: ", part2_sol)


if __name__ == "__main__":
    main()
