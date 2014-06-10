from PIL import Image


class BitmapData:

    def __init__(self, pixels, w, h):
        self.pixels = pixels
        self.width = w
        self.height = h

    @classmethod
    def fromFileImage(cls, image_path):
        i = Image.open(image_path)
        monochrome = i.convert('1')
        data = monochrome.getdata()
        pixels = []
        for i in range(len(data)):
            if data[i] == 255:
                pixels.append(0)
            else:
                pixels.append(1)
        (w, h) = monochrome.size
        return cls(pixels, w, h)