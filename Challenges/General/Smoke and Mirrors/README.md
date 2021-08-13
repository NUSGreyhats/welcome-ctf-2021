# Challenge Details

A binary file - `flag.exe` - has been hidden in `image.png` via
[LSB-Steganography](https://youtu.be/TWEXCYQKyDc)! It is known
that `flag.exe` is 11,392 bytes large. Also, the file is spread
across the first N pixels of the image when traversing in
[row-major order](https://en.wikipedia.org/wiki/Row-_and_column-major_order).

Can you recover the executable and uncover the flag?

# Setup Instructions

Download `image.png`.

# Possible Hints

Use the `Pillow` module in `Python`.

# Key Concepts

1. LSB-Steganography
2. Scripting

# Solution

Write a script to extract the first `8,648 * 8` LSBs of the
image and write that bit string to a `.exe` file. Run said
executable.

A proposed solution can be found in `solution.py`.

# Learning Objectives

1. Steganography is the art of hiding things in plain sight.
2. Changing the LSBs of an image makes an imperceptible difference.
3. Use `Pillow` to work with an image at pixel level.

# Flag

`greyhats{m0r3_th6n_m33t5_the_3y3_189794872}`
