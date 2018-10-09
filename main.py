from __future__ import absolute_import, unicode_literals
import png, array

print("Setting up")

reader = png.Reader(filename='challenge.png')
w, h, pixels, metadata = reader.read_flat()

pixel_byte_width = 4 if metadata['alpha'] else 3
result_pixels = pixels[:]

row310 = [0] * w

print("Detecting steganography")

for i in range(0, len(pixels), pixel_byte_width):
    if(pixels[i] != pixels[i+1] or pixels[i+1] != pixels[i+2] or pixels[i] != pixels[i+2]):
        result_pixels[i+0] = 0
        result_pixels[i+1] = 0
        result_pixels[i+2] = 0

        x = int((i/pixel_byte_width) % w)
        y = int((i/pixel_byte_width) / w)
        if y == 310:
            row310[x] = 1
    else:
        result_pixels[i+0] = 255
        result_pixels[i+1] = 255
        result_pixels[i+2] = 255


print("Saving steganography image")

output = open('challenge-2.png', 'wb')
writer = png.Writer(w, h, **metadata)
writer.write_array(output, result_pixels)
output.close()


print("Row 310 bits")
row310_bytes = []
for i in range(0, len(row310), 8):
    row310_bytes.append(int(''.join(str(x) for x in row310[i:i+8]), 2))
print(row310_bytes)

row310_image = []
for byte in row310_bytes:
    row310_image.append(byte)
    row310_image.append(byte)
    row310_image.append(byte)

output = open('challenge-3.png', 'wb')
writer = png.Writer(16, 23)
writer.write_array(output, row310_image)
output.close()

# Possible image sizes
# 1  , 2  , 4 , 8 , 16, 23, 46, 92, 184, 368
# 368, 184, 92, 46, 23, 16, 8 , 4 , 2  , 1

print("Done")
