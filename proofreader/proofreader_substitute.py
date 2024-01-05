from proofreader_tui import read_file
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py proofread_filename original_filename")
        sys.exit(1)

    sentence_pairs = read_file(sys.argv[1])
    with open(sys.argv[2], "r", encoding="utf-8") as file:
        original_text = file.read()

    for pair in sentence_pairs:
        if pair.status == "b":
            original_text = original_text.replace(pair.original, pair.modified)
    with open(sys.argv[2], "w", encoding="utf-8") as file:
        file.write(original_text)
        return


if __name__ == "__main__":
    main()
