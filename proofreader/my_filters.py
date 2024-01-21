import re

def qmd_to_txt(text):
    lines = text.split('\n')

    # Remove YAML
    assert lines[0].strip() == '---', "First line should be exactly '---'."
    end_yaml_index = lines.index('---', 1)
    del lines[0:end_yaml_index + 1]

    # Remove code blocks
    head_numbers = [i for i, line in enumerate(lines) if re.match(r'^\s*```{?=?[a-zA-Z].*\s*$', line)]
    tail_numbers = [i for i, line in enumerate(lines) if re.match(r'^\s*```\s*$', line)]

    assert len(head_numbers) == len(tail_numbers), f"\n{head_numbers}\nand\n{tail_numbers}\nare mismatched"
    for i in range(len(head_numbers)):
        assert head_numbers[i] < tail_numbers[i], f"""codeblock is malformed between lines:
        {lines[head_numbers[i]]}
        {lines[tail_numbers[i]]}"""
        if i < len(head_numbers) - 1:
            assert tail_numbers[i] < head_numbers[i + 1], f"""codeblock is malformed between lines:
        {lines[tail_numbers[i]]}
        {lines[head_numbers[i + 1]]}"""

    for i in range(len(head_numbers) - 1, -1, -1):
        del lines[head_numbers[i]:tail_numbers[i] + 1]

    # Check that all codeblocks are removed
    for line in lines:
        assert not re.match(r'^```.*$', line), f"bad line:\n{line}"
    
    # Remove blockquotes and other formattings
    lines = filter(lambda line: not re.match(r'{{<.*>}}', line), lines)
    lines = filter(lambda line: not re.match(r'^\s*> .*$', line), lines)
    lines = filter(lambda line: not re.match(r'^\s*>\s*$', line), lines)

    # Keep only image captions.
    lines = map(lambda line: re.sub(r"\!\[(.*)\]\(.*\).*", r"\1", line), lines)
    # Remove urls and links
    lines = map(lambda line: re.sub(r"\]\(.*\)", r"]", line), lines)
    lines = map(lambda line: re.sub(r"<.*>", r"", line), lines)

    # Remove extra lines
    lines = '\n'.join(lines)
    lines = re.sub(r"\n\n+", r"\n\n", lines)
    return lines
