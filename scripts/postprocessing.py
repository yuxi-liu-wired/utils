def process_output_file(filename="output.md"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Split the content into a list of strings based on "$$ ... $$" pattern
    parts = content.split("$$")

    # Process each part
    processed_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Odd indices contain the content within "$$ ... $$"
            stripped_content = part.strip()
            processed_parts.append(f"\n\n$$\n{stripped_content}\n$$\n\n")
        else:
            processed_parts.append(part.strip())

    # Join the processed parts back into a single string
    processed_content = "".join(processed_parts)

    # Write the processed content back to the file
    with open(filename, "w", encoding="utf-8") as f:
        f.write(processed_content)


if __name__ == "__main__":
    process_output_file()
