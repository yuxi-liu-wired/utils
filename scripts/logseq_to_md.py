import re


def main():
    fname = "input.md"

    with open(fname, "r") as f:
        temp = f.read()

    # general clean-up
    temp = re.sub(r"^[ \t]*- ", "\n", temp)
    temp = re.sub(r"\$ ([\.,!;:?])", r"$\1", temp)
    temp = re.sub(r"collapsed:: true", "", temp)

    # thm, prop, proof
    temp = re.sub(r"PROP\.", "::: {#prp-todo}\n\n## \n\n:::", temp)
    temp = re.sub(r"THM\.", "::: {#thm-todo}\n\n## \n\n:::", temp)
    temp = re.sub(r"COR\.", "::: {#cor-todo}\n\n## \n\n:::", temp)
    temp = re.sub(r"LEMMA\.", "::: {#thm-todo}\n\n## \n\n:::", temp)
    temp = re.sub(r"PROOF\.", "::: {.proof}\n\n## \n\n:::", temp)

    temp = re.sub(r"WARN\.", "::: {.callout-warning}\n\n:::", temp)
    temp = re.sub(r"COMM\.", "::: {.callout-tip}\n\n:::", temp)
    temp = re.sub(r"INTP\.", '::: {.callout-note title="Interpretation"}\n\n:::', temp)
    temp = re.sub(r"NOTE\.", "::: {.callout-note}\n\n:::", temp)

    # my math shorthands
    temp = re.sub(r"(?i)(wolog)", r"WLOG", temp)
    temp = re.sub(r"wirt", r"with respect to", temp)
    temp = re.sub(r"bequl", r"the following are equivalent", temp)
    temp = re.sub(r"cone\(", r"\\mathrm\{Cone\}(", temp)
    temp = re.sub(r"E(_\{[^\}]*})\[", r"\\mathbb\{E\}\1\[", temp)
    temp = re.sub(r"D\(([^;]+);([^\)]+)\)", r"D(\1 \\\| \2)", temp)

    # general clean-up
    temp = re.sub(r"\$\$\s+- ", r"$$\n\n", temp)
    temp = re.sub(r"\$\$\s+", r"$$\n\n", temp)
    temp = re.sub(r"^\t+ *-?", r"\n", temp, flags=re.MULTILINE)
    temp = re.sub(r"^\s+$", "", temp, flags=re.MULTILINE)
    temp = re.sub(r"^-", "", temp, flags=re.MULTILINE)
    temp = re.sub(r"^\s+([A-Za-z].*)$", r"\n\n\1", temp, flags=re.MULTILINE)
    temp = re.sub(r"\n\n+", r"\n\n", temp)

    # Output to "output.md"
    with open("output.md", "w") as outfile:
        outfile.write(temp)


if __name__ == "__main__":
    main()
