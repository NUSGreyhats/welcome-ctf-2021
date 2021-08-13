from PIL import Image

# We cannot extract the LSBs from the binary directly
# as images often contain headers and (in the case of
# .png files) are losslessly compressed when saved to
# disk.
# 
# Use any image editing software to read and unpack
# the binary into actual pixels and then extract the
# LSBs from the resulting MxN array.
FILE = input('Filename: ')
im = Image.open(FILE)


# Get the dimensions of the image, i.e. M and N.
width, height = im.size


# How many LSBs to extract?
binary_size_in_bytes = int(input('Original file size (bytes): '))
binary_size_in_bits  = binary_size_in_bytes * 8


# Extraction function.
def extract_lsb(image, num_lsbs):
    bit_string = []

    for i in range(height):
        for j in range(width):
            pixel_value  = image.getpixel((j, i))
            pixel_lsb    = pixel_value & 1

            bit_string.append(pixel_lsb)

            if len(bit_string) == num_lsbs:
                return bit_string

bit_string = extract_lsb(im, binary_size_in_bits)


# Convert to byte array for writing.
byte_file = []

for i in range(0, binary_size_in_bits, 8):
    byte = 0

    for j in range(8):
        byte <<= 1
        byte += bit_string[i + j]

    byte_file.append(byte)


# Write binary to disk.
with open('flag.exe', 'wb') as fd:
    fd.write(bytes(byte_file))
