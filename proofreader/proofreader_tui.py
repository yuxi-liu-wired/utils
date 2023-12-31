from blessed import Terminal
import difflib
import sys
from dataclasses import dataclass, replace
import textwrap


@dataclass
class SentencePair:
    original: str
    modified: str
    status: str
    reason: str = ""

    def __str__(self):
        a = ("[a]" if self.status == "a" else "a") + f": {self.original}"
        b = ("[b]" if self.status == "b" else "b") + f": {self.modified}"
        reason = f"\nc: {self.reason}" if self.reason else ""
        return f"{a}\n{b}{reason}\n\n"


def read_file(file_path):
    sentence_pairs = []
    with open(file_path, "r") as file:
        lines = list(filter(lambda x: x.strip(), file.readlines()))
        i = 0
        while i < len(lines):
            orig_line = lines[i].strip()
            mod_line = lines[i + 1].strip()
            if i + 2 < len(lines) and lines[i + 2].strip().startswith("c:"):
                reason = lines[i + 2].strip()[2:].strip()
                i += 3
            else:
                reason = ""
                i += 2

            if orig_line.startswith("[a]:"):
                status = "a"
                orig_line = orig_line[4:].strip()
            elif orig_line.startswith("a:"):
                status = "undecided"
                orig_line = orig_line[2:].strip()
            else:
                raise ValueError(f"Invalid line {orig_line}. Expected [a]: or a:")
            if mod_line.startswith("[b]:"):
                status = "b"
                mod_line = mod_line[4:].strip()
            elif mod_line.startswith("b:"):
                mod_line = mod_line[2:].strip()
            else:
                raise ValueError(f"Invalid line {mod_line}. Expected [b]: or b:")

            pair = SentencePair(
                original=orig_line, modified=mod_line, status=status, reason=reason
            )
            sentence_pairs.append(pair)
    # Filter out sentences that are equal
    sentence_pairs = [pair for pair in sentence_pairs if pair.original != pair.modified]
    return sentence_pairs


def split_into_chunks(text, chunk_size):
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def display_pairs(t, pairs, current_index):
    if current_index < 0 or current_index >= len(pairs):
        return
    pair = pairs[current_index]

    # Number of pairs whose status is undecided
    undecided_count = len([p for p in pairs if p.status == "undecided"])

    # Calculate diff
    diff = list(difflib.ndiff([pair.original], [pair.modified]))
    if len(diff) == 1:
        diff = [diff[0], "", diff[0], ""]
    elif len(diff) == 2:
        diff = [diff[0], "", diff[1], ""]
    elif len(diff) == 3:
        if diff[1].startswith("?"):
            diff = [diff[0], diff[1], diff[2], ""]
        else:
            diff = [diff[0], "", diff[1], diff[2]]
    # Padding
    diff[1] += " " * (len(diff[0]) - len(diff[1]))
    diff[3] += " " * (len(diff[2]) - len(diff[3]))

    # Display the original and modified texts with background color
    status_1 = f"Editing: {current_index + 1}/{len(pairs)}"
    status_2 = f"Pairs left: {undecided_count}/{len(pairs)}"
    status = status_1 + " " * (t.width - len(status_1) - len(status_2)) + status_2
    print(t.black_on_bright_white(status))

    fa = t.bright_red_on_bright_black if pair.status == "a" else t.bright_red_on_black
    fb = (
        t.bright_green_on_bright_black
        if pair.status == "b"
        else t.bright_green_on_black
    )

    wrap_width = min(144, t.width - 4)
    diff0 = textwrap.wrap(diff[0], wrap_width)
    diff1 = []
    for d in diff0:
        l = len("".join(diff1))
        diff1.append(diff[1][l : l + len(d)])
    diff2 = split_into_chunks(diff[2], wrap_width)
    diff3 = []
    for d in diff2:
        l = len("".join(diff3))
        diff3.append(diff[3][l : l + len(d)])

    print(t.move_y(4))
    for i, (line0, line1) in enumerate(zip(diff0, diff1)):
        print(t.move_xy(2, 4 + 2 * i) + fa(line0))
        print(t.move_x(2, 4 + 2 * i + 1) + t.bright_red_on_black(line1))
    # print(t.move_y(4 + 2 * len(diff0) + 1))
    for i, (line2, line3) in enumerate(zip(diff2, diff3)):
        print(t.move_xy(2, 4 + 2 * len(diff0) + 1 + 2 * i) + fb(line2))
        print(
            t.move_xy(2, 4 + 2 * len(diff0) + 1 + 2 * i + 1)
            + t.bright_green_on_black(line3)
        )

    print("\n\n" + t.move_x(2) + pair.reason)


def save_pairs(filename, pairs):
    with open(f"{filename}", "w") as f:
        text = "".join(map(str, pairs))
        f.write(text)


def handle_keypress(t, key, pairs, current_index):
    if key.code == t.KEY_LEFT:
        if current_index == 0:
            return len(pairs) - 1
        else:
            return current_index - 1
    elif key.code == t.KEY_RIGHT:
        if current_index == len(pairs) - 1:
            return 0
        else:
            return current_index + 1
    elif key.code == t.KEY_UP:
        pairs[current_index] = replace(pairs[current_index], status="a")
        return current_index
    elif key.code == t.KEY_DOWN:
        pairs[current_index] = replace(pairs[current_index], status="b")
        return current_index
    elif key == " ":
        pairs[current_index] = replace(pairs[current_index], status="undecided")
    elif key.code == t.KEY_ENTER:
        try:
            return next(
                (
                    i
                    for i, p in enumerate(pairs)
                    if p.status == "undecided" and i > current_index
                )
            )
        except StopIteration:
            try:
                return next((i for i, p in enumerate(pairs) if p.status == "undecided"))
            except:
                raise StopIteration
    return current_index


def display_help(t):
    help_str = """    arrow keys: navigate
    space: un-decide a pair
    enter: jump to the next undecided pair
    w: write
    q: quit   Q: quit without asking for save"""
    print(t.move_y(t.height - len(help_str.split("\n")) - 2))
    print(t.bright_white_on_black(help_str))


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py filename")
        sys.exit(1)

    filename = sys.argv[1]
    t = Terminal()
    sentence_pairs = read_file(filename)
    current_index = 0

    with t.cbreak(), t.hidden_cursor():
        while True:
            print(t.home + t.clear)
            display_pairs(t, sentence_pairs, current_index)

            key = t.inkey()
            if key == "q":
                print(t.move_xy(2, t.height - 2) + "Save first? (y)es/(n)o/(c)ancel")
                while key not in "ync":
                    key = t.inkey()
                if key == "c":
                    continue
                elif key == "y":
                    save_pairs(filename, sentence_pairs)
                print(t.home + t.clear)
                sys.exit(0)
            elif key == "Q":
                print(t.home + t.clear)
                sys.exit(0)
            elif key == "w":
                save_pairs(filename, sentence_pairs)
            elif key == "h":
                display_help(t)
            else:
                try:
                    current_index = handle_keypress(
                        t, key, sentence_pairs, current_index
                    )
                except StopIteration:
                    print(
                        t.home
                        + t.move_xy(0, t.height // 2)
                        + t.black_on_bright_blue(full_width(t, "  All pairs decided!"))
                    )
                    t.inkey()


def full_width(t, text):
    return text + " " * (t.width - len(text))


if __name__ == "__main__":
    main()
