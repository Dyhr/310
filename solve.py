import png, hashlib


def loadImage(path):
    reader = png.Reader(filename=path)
    w, h, pixels, metadata = reader.read_flat()
    byte_width = 4 if metadata['alpha'] else 3
    return w, h, pixels, metadata, byte_width

def saveImage(path, pixels, w, h, metadata):
    output = open(path, 'wb')
    if metadata == None:
        writer = png.Writer(w, h)
    else:
        writer = png.Writer(w, h, **metadata)
    writer.write_array(output, pixels)
    output.close()

def sha256(text):
    return hashlib.sha256(text.encode("ascii")).hexdigest()

def processImage(pixels, byte_width, w, h, func):
    for i in range(0, len(pixels), byte_width):
        x = int((i/byte_width) % w)
        y = int((i/byte_width) / w)
        pixel = [pixels[i+j] for j in range(0,byte_width)]
        func(i,x,y,pixel)

def setPixel(pixels, i, pixel):
    for p in range(0, len(pixel)):
        pixels[i+p] = pixel[p]


def mask(pixel, mask):
    if len(pixel) == len(mask):
        return [(255-pixel[i]) & int(mask[i],2) for i in range(0,len(pixel))]
    else:
        return None
