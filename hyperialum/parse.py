def parse(self, input_file):
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
