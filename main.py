from __future__ import absolute_import, unicode_literals
import png, array, hashlib

print("Setting up")

reader = png.Reader(filename='challenge.png')
w, h, pixels, metadata = reader.read_flat()

pixel_byte_width = 4 if metadata['alpha'] else 3
alpha_pixels = pixels[:]
gray_pixels = pixels[:]

row310 = [0] * w

print("Processing")

for i in range(0, len(pixels), pixel_byte_width):
    x = int((i/pixel_byte_width) % w)
    y = int((i/pixel_byte_width) / w)
    pixel = [pixels[i+0], pixels[i+1], pixels[i+2], pixels[i+3]]
    mask = [
        (255-pixel[0]) & int('00000000',2),
        (255-pixel[1]) & int('00000000',2),
        (255-pixel[2]) & int('00000000',2),
        (255-pixel[3]) & int('00000001',2),
    ]
    
    if sum(mask) != 0:
        alpha_pixels[i+0] = 0
        alpha_pixels[i+1] = 0
        alpha_pixels[i+2] = 0
        
        if y == 310:
            row310[x] = 1
        #print(str(x)+" "+str(y)+" "+bin(diff))
    else:
        alpha_pixels[i+0] = 255
        alpha_pixels[i+1] = 255
        alpha_pixels[i+2] = 255

    if pixel[0] == pixel[1] and pixel[1] == pixel[2]:
        if pixel[0] > 0 and pixel[0] < 255:
            gray_pixels[i+0] = round(pixel[0]/255)*255
            gray_pixels[i+1] = round(pixel[1]/255)*255
            gray_pixels[i+2] = round(pixel[2]/255)*255
        #else:
        #    gray_pixels[i+0] = 0
        #    gray_pixels[i+1] = 0
        #    gray_pixels[i+2] = 0


print("Saving steganography image")

output = open('challenge-2.png', 'wb')
writer = png.Writer(w, h, **metadata)
writer.write_array(output, alpha_pixels)
output.close()


print("Saving noise")

output = open('challenge-3.png', 'wb')
writer = png.Writer(w, h, **metadata)
writer.write_array(output, gray_pixels)
output.close()


print("Row 310 message 1:")

row310_bytes = []
for i in range(0, len(row310), 8):
    row310_bytes.append(int(''.join(str(1-x) for x in row310[i:i+8]), 2))

row310_message = ''.join([str(chr(b)) if b != 255 else "" for b in row310_bytes])

print(row310_message)

#print(hashlib.sha256(row310_message.encode("ascii")).hexdigest())


print("Done")

# L503K7CF64C120E89D9D4
