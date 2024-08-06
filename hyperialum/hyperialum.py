import re
import argparse
from . import loop, parse


class Hyperialum:

    def __init__(self, file, input_file, parameters=[]):
        self.variables = {}
        self.output = []
        self.file = file
        self.is_selector_open = False
        self.parameters = parameters
        self.parse(input_file)

    def _handle_parameters(self):
        for param in self.parameters:
            if param == "compact":
                compacted_output = self._compact("\n".join(self.output))
                self.output = [compacted_output]

    def parse(self, input_file):
        parse.parse(self, input_file)

    def _handle_variable(self, line):
        name, value = line.split(":", 1)
        name = name.strip()[1:]
        value = value.strip().strip(";")
        self.variables[name] = value

    def _handle_selector(self, line):
        if self.is_selector_open:
            self.output.append("}")
        selector = line.strip()
        self.output.append(f"{selector} {{")
        self.is_selector_open = True

    def _handle_property(self, line):
        property_name, value = line.split(":", 1)
        property_name = property_name.strip()
        value = value.strip().rstrip(";")
        if value.startswith("$"):
            value = self.variables.get(value[1:], value)
        self.output.append(f"    {property_name}: {value};")

    def _handle_for_loop(self, lines, i):
        loop.loop(self, lines, i)

    def _handle_comments(self, line):
        comments = ["//", ">>"]
        for comment in comments:
            if comment in line:
                line = line.split(comment, 1)[0]
                break
        return line.strip()

    def _compact(self, code):
        code = code.replace("\n", " ")
        code = re.sub("\\s+", " ", code)
        return code.strip()

    def write_file(self):
        self._handle_parameters()
        with open(self.file, "w") as f:
            f.write("\n".join(self.output))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_file", help="Input file")
    ap.add_argument("--output_file", action="store", help="Output file")
    ap.add_argument("--compact", action="store_true", help="Compact the output CSS")
    args = ap.parse_args()
    parameters = []
    if not args.input_file:
        ap.print_help()
        return
    if not args.input_file.endswith(".hym"):
        print("Input file should be a .hym file")
        return
    output_file = (
        args.output_file
        if args.output_file
        else args.input_file.replace(".hym", ".css")
    )
    if args.compact:
        parameters.append("compact")
    hym = Hyperialum(output_file, args.input_file, parameters)
    hym.write_file()


if __name__ == "__main__":
    main()
