from PIL import Image

class BitmapData:

    def __init__(self, pixels, w, h):
        self.pixels = pixels
        self.width = w
        self.height = h

    @classmethod
    def fromFileImage(cls, image_path):
        i = Image.open(image_path)
        (w, h) = i.size
        if w > 512:
            ratio = int(w / 512)
            h = int(h / ratio)
            i = i.resize((512, h), Image.ANTIALIAS)
        i = i.convert('1')
        data = i.getdata()
        pixels = []
        for i in range(len(data)):
            if data[i] == 255:
                pixels.append(0)
            else:
                pixels.append(1)
        return cls(pixels, w, h)
