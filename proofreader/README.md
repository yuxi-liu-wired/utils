# `proofreader_tui.py`

## 1. File Processing

Read and process the file into a list of named tuples. Each tuple will represent a sentence pair along with its status.

### File Format

* Each pair is separated into two parts: `a` for original and `b` for modified.
* The status is indicated by square brackets around `a` or `b`.

### Code Structure

* Define a named tuple for storing sentence pairs.
* Read the file line by line.
* Extract `original`, `modified`, and `status` for each pair.
* Store these in a list of named tuples.

## 2. Displaying Content

Split the screen into two columns using Blessed's layout capabilities.

### Display Structure

* Left column for the original sentence.
* Right column for the modified sentence.
* Highlight differences using a `diff` tool.

## 3. User Interaction

Implement key bindings for various functions.

### Key Bindings

* `<LEFT>`: Move to the previous sentence pair.
* `<RIGHT>`: Move to the next sentence pair.
* `<SPACE>`: Jump to the next undecided pair. Display a message if all pairs are decided.
* `<ESC>`: Mark the current pair as undecided.
* `:<w>`: Overwrite the original file with current data.
* `:<q>`: Quit the program.
