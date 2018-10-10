from __future__ import absolute_import, unicode_literals
import array
import solve


print("Setting up")

w, h, pixels, metadata, byte_width = solve.loadImage('challenge.png')

alpha_pixels = pixels[:]
gray_pixels = pixels[:]

row310 = [0] * w
col310 = [0] * h


print("Processing image")

def process(i,x,y,pixel):
    mask = solve.mask(pixel, ['00000000','00000000','00000000','00000001'])
    
    if sum(mask) != 0:
        solve.setPixel(alpha_pixels, i, [0,0,0])
        
        if y == 310:
            row310[x] = 1
    else:
        solve.setPixel(alpha_pixels, i, [255,255,255])

    if pixel[0] == pixel[1] and pixel[1] == pixel[2]:
        if pixel[0] > 0 and pixel[0] < 255:
            solve.setPixel(gray_pixels, i, [round(pixel[0]/255)*255, round(pixel[1]/255)*255, round(pixel[2]/255)*255])

solve.processImage(pixels,byte_width,w,h,process)


print("Solving the grid")
grid_key = "20181002"
grid_message = "511 B20 332 328 410 530 22B 0FE 52E D0F 7A1 65B 52C 7E7 511 2F6 56F C4B"
grid_shifted = solve.shiftKey(grid_message, grid_key)
grid_numbers = [int(grid_shifted[i:i+4],16) for i in range(0,len(grid_shifted),4)][6:]
grid_words = ' '.join([solve.lookupBip36(n) for n in grid_numbers])

print(f"{grid_message} ->\n{grid_shifted} ->\n{grid_numbers} ->\n{grid_words}")


print("Saving steganography image")
solve.saveImage('challenge-2.png', alpha_pixels, w, h, metadata)


print("Saving noiseless")
solve.saveImage('challenge-3.png', gray_pixels, w, h, metadata)


print("Row 310 Message 1:")
row310_bytes = []
for i in range(0, len(row310), 8):
    row310_bytes.append(int(''.join(str(1-x) for x in row310[i:i+8]), 2))

row310_message = ''.join([str(chr(b)) if b != 255 else "" for b in row310_bytes])

print(row310_message)

#print(hashlib.sha256(row310_message.encode("ascii")).hexdigest())


print("Done")

# L503K7CF64C120E89D9D4
# 310 -> chase
