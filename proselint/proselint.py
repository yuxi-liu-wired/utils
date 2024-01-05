import re
import sys
import json
import panflute as pf

def colored(text, color):
    color_dict = {
        "red": ("\033[91m", "\033[0m"),
        "green": ("\033[92m", "\033[0m"),
        "yellow": ("\033[93m", "\033[0m"),
        "blue": ("\033[94m", "\033[0m"),
    }
    start, end = color_dict[color]
    return f"{start}{text}{end}"


def highlight_match(text, match, color, reason=""):
    start_context = max(0, match.start() - 30)
    end_context = min(len(text), match.end() + 30)

    before_match = text[start_context : match.start()].split("\n")[-1]
    matched_text = text[match.start() : match.end()]
    after_match = text[match.end() : end_context].split("\n")[0]

    highlighted_match = f"{before_match}{colored(matched_text, color)}{after_match}"
    line_number = text[: match.start()].count("\n") + 1
    char_number = match.start() - text[: match.start()].rfind("\n")
    print(f"line {line_number}, char {char_number}: {reason}")
    print(highlighted_match + "\n")


def quotation_lint(text):
    """Check for logical quotation standards.

    Examples:
    They stated "MLPs are essentially Gamba perceptrons."
    ->
    They stated "MLPs are essentially Gamba perceptrons.".

    In the next section, using the "pebble construction," they studied "Gamba perceptrons."
    ->
    In the next section, using the "pebble construction", they studied "Gamba perceptrons".
    """
    pattern = re.compile(r'([?.,;:!])"([^?.,;:!$]|$)')
    matches = pattern.finditer(text)
    print("Checking for logical quotation standards...\n")
    for match in matches:
        highlight_match(text, match, "blue")


def typo_lint(text):
    print("Checking for common typos...\n")
    file_path = "common_typos.json"
    try:
        with open(file_path, "r") as file:
            json_file = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return
    for rule in json_file:
        pattern = rule["a"].strip()
        search_pattern = rf"{pattern}"
        reason = rule["reason"].strip()
        matches = re.finditer(search_pattern, text)
        for match in matches:
            highlight_match(text, match, "red", reason)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        filename = sys.argv[1]
        try:
            with open(filename, "r") as file:
                text = file.read()
                if filename.endswith(".qmd"):
                    print(
                        f"Consider running `quarto render {filename} --to plain` first.".strip()
                    )
                quotation_lint(text)
                typo_lint(text)

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
