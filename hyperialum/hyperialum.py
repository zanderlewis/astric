import re
import argparse


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
        print(f"Reading input file: {input_file}")
        with open(input_file) as f:
            code = f.read()
        lines = code.splitlines()
        i = 0
        while i < len(lines):
            stripped_line = self._handle_comments(lines[i])
            if not stripped_line:
                i += 1
                continue
            if stripped_line.startswith("$"):
                self._handle_variable(stripped_line)
            elif stripped_line.startswith("--for"):
                i = self._handle_for_loop(lines, i)
            elif ":" in stripped_line:
                self._handle_property(stripped_line)
            else:
                self._handle_selector(stripped_line)
            i += 1
        if self.is_selector_open:
            self.output.append("}")
        return "\n".join(self.output)

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
        loop_line = lines[i].strip()
        match = re.match(
            "--for\\s+\\$(\\w+)\\s+from\\s+(\\d+)\\s+to\\s+(\\d+)", loop_line
        )
        if match:
            var_name = match.group(1)
            start = int(match.group(2))
            end = int(match.group(3))
            loop_body = []
            i += 1
            while i < len(lines) and (not lines[i].strip().startswith("--endfor")):
                loop_body.append(lines[i].strip())
                i += 1
            for j in range(start, end + 1):
                for line in loop_body:
                    replaced_line = line.replace(f"${var_name}", str(j))
                    if ":" in replaced_line:
                        self._handle_property(replaced_line)
                    else:
                        if self.is_selector_open:
                            self.output.append("}")
                            self.is_selector_open = False
                        self._handle_selector(replaced_line)
            if self.is_selector_open:
                self.output.append("}")
                self.is_selector_open = False
        return i

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
        print(f"Writing output file: {self.file}")
        with open(self.file, "w") as f:
            f.write("\n".join(self.output))
        print(f"Output written to {self.file}")


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
