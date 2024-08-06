import re


def loop(self, lines, i):
    loop_line = lines[i].strip()
    match = re.match("--for\\s+\\$(\\w+)\\s+from\\s+(\\d+)\\s+to\\s+(\\d+)", loop_line)
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
