from __future__ import absolute_import, unicode_literals
import array, base64, gzippy
import solve

def grid():
    print("Solving the grid")
    grid_key = "20181002"
    grid_message = "511 B20 332 328 410 530 22B 0FE 52E D0F 7A1 65B 52C 7E7 511 2F6 56F C4B"
    grid_shifted = solve.shiftKey(grid_message, grid_key)
    grid_numbers = [int(grid_shifted[i:i+4],16) for i in range(0,len(grid_shifted),4)][6:]
    grid_words = ' '.join([solve.lookupBip36(n) for n in grid_numbers])

    print(f"{grid_message} ->\n{grid_shifted} ->\n{grid_numbers} ->\n{grid_words}")

def alphaMessage():
    print("Setting up")

    w, h, pixels, metadata, byte_width = solve.loadImage('challenge.png')

    alpha_pixels = pixels[:]

    row310 = [0] * w


    print("Processing image")

    def process(i,x,y,pixel):
        mask = solve.mask(pixel, ['00000000','00000000','00000000','00000001'])
        
        if sum(mask) != 0:
            solve.setPixel(alpha_pixels, i, [0,0,0])
            
            if y == 310:
                row310[x] = 1
        else:
            solve.setPixel(alpha_pixels, i, [255,255,255])
            
    solve.processImage(pixels,byte_width,w,h,process)


    print("Saving steganography image")
    solve.saveImage('challenge-alpha.png', alpha_pixels, w, h, metadata)


    print("Row 310 Alpha Message:")
    row310_bytes = []
    for i in range(0, len(row310), 8):
        row310_bytes.append(int(''.join(str(1-x) for x in row310[i:i+8]), 2))

    row310_message = ''.join([str(chr(b)) if b != 255 else "" for b in row310_bytes])

    print(row310_message)
    
def redMessage():
    print("Setting up")

    w, h, pixels, metadata, byte_width = solve.loadImage('challenge.png')

    red_pixels = pixels[:]

    row310_red = [0] * w
    row310_alpha = [1] * w


    print("Processing image")

    def process(i,x,y,pixel):
        mask_alpha = solve.mask(pixel, ['00000000','00000000','00000000','00000001'])
        mask_red = solve.mask(pixel, ['00000001','00000000','00000000','00000000'])
        
        if mask_alpha[3] == 1 and y == 310:
            row310_alpha[x] = 0

        if y == 310:
            row310_red[x] = 1-mask_red[0]

        if pixel[0] != pixel[1] or pixel[0] != pixel[2]:
            solve.setPixel(red_pixels, i, [0,0,0])
        else:
            solve.setPixel(red_pixels, i, [255,255,255])
            
    solve.processImage(pixels,byte_width,w,h,process)


    print("Saving steganography image")
    solve.saveImage('challenge-red.png', red_pixels, w, h, metadata)


    print("XORing bits.. Resulting base 64:")
    xor_bits = [row310_red[i] ^ row310_alpha[i] for i in range(0,w)]

    row310_bytes = [int(''.join(str(1-x) for x in xor_bits[i:i+8]), 2) for i in range(0, len(xor_bits), 8)]

    row310_b64 = base64.b64encode(bytes(row310_bytes[:-121]))#''.join([str(chr(b)) for b in row310_bytes])
    print(str(row310_b64))

    #print([str(chr(b)) if b != 255 else "" for b in row310_bytes])

def noise():
    print("Setting up")

    w, h, pixels, metadata, byte_width = solve.loadImage('challenge.png')

    gray_pixels = pixels[:]


    print("Processing image")

    def process(i,x,y,pixel):
        if pixel[0] == pixel[1] and pixel[1] == pixel[2]:
            if pixel[0] > 0 and pixel[0] < 255:
                solve.setPixel(gray_pixels, i, [round(pixel[0]/255)*255, round(pixel[1]/255)*255, round(pixel[2]/255)*255])

    solve.processImage(pixels,byte_width,w,h,process)

    print("Saving noiseless")
    solve.saveImage('challenge-3.png', gray_pixels, w, h, metadata)
