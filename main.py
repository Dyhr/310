from __future__ import absolute_import, unicode_literals
import png, array


reader = png.Reader(filename='challenge.png')
w, h, pixels, metadata = reader.read_flat()

pixel_byte_width = 4 if metadata['alpha'] else 3
#pixel_position = point[0] + point[1] * w
new_pixel_value = (255, 0, 0, 0) if metadata['alpha'] else (255, 0, 0)

mismatches = 0
for i in range(0, len(pixels), pixel_byte_width):
    if(pixels[i] != pixels[i+1] or pixels[i+1] != pixels[i+2] or pixels[i] != pixels[i+2]):
        print(f"{pixels[i]} {pixels[i+1]} {pixels[i+2]} {pixels[i+3]}")
        mismatches = mismatches + 1

print(mismatches)

#output = open('image-with-red-dot.png', 'wb')
#writer = png.Writer(w, h, **metadata)
#writer.write_array(output, pixels)
#output.close()
