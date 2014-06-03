__author__ = 'benoit'

import usb.core

class Epson_Thermal(object):

    printer = None

    def __init__(self, idVendor, idProduct, interface=0, in_ep=0x82, out_ep=0x01):
        """
        @param idVendor  : Vendor ID
        @param idProduct : Product ID
        @param interface : USB device interface
        @param in_ep     : Input end point
        @param out_ep    : Output end point
        """
        self.idVendor  = idVendor
        self.idProduct = idProduct
        self.interface = interface
        self.in_ep     = in_ep
        self.out_ep    = out_ep

        # Search device on USB tree and set is as printer
        self.printer = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if self.printer is None:
            print "Cable isn't plugged in"

        if self.printer.is_kernel_driver_active(0):
            try:
                self.printer.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print "Could not detatch kernel driver: %s" % str(e)

        try:
            self.printer.set_configuration()
            self.printer.reset()
        except usb.core.USBError as e:
            print "Could not set configuration: %s" % str(e)

    def _write(self, msg):
        self.printer.write(self.out_ep, msg, self.interface)


    def linefeed(self):
        self._write(chr(10)) # LF

    def print_text(self, msg):
        self._write(msg)

    def cut(self):
        byte_array = [
            chr(29), # GS
            chr(86), # V
            chr(0)]  # \0
        command = ''.join(byte_array)
        self._write(command)

    def print_bitmap(self, pixels, w, h):

        # Set line spacing to 24 dots
        byte_array = [
            chr(27),    # ESC
            chr(51),    # 3
            chr(24)]
        self._write(''.join(byte_array))


        # Calculate nL and nH
        nh = chr(w / 256)
        nl = chr(w % 256)

        offset = 0

        while offset < h:
            byte_array = [
                chr(27),  # ESC
                chr(42),  # *
                chr(33),  # double density mode
                nl,
                nh]

            for x in range(w):
                for k in range(3):
                    slice = 0
                    for b in range(8):
                        y = (((offset / 8) + k) * 8) + b
                        i = (y * w) + x
                        v = 0
                        if i < len(pixels):
                            v = pixels[i]
                        slice |= (v << (7 - b))

                    byte_array.append(chr(slice))

            offset += 24
            self._write(''.join(byte_array))
            self.linefeed()


        # Restore the line spacing to the default 30 dots
        byte_array = [
            chr(27),    # ESC
            chr(51),    # 3
            chr(30)]
        self._write(''.join(byte_array))

    def get_pixels_and_dimensions(self, image_path):
        import Image
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
        return (pixels, w, h)



if __name__ == '__main__':
    printer = Epson_Thermal(0x04b8,0x0e03)  # EPSON TM-T20
    printer.print_text("Hello world")
    printer.linefeed()
    (pixels, w, h) = printer.get_pixels_and_dimensions("logo.png")
    printer.print_bitmap(pixels, w, h)
    printer.linefeed()
    printer.cut()
