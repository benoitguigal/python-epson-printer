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
            print("Cable isn't plugged in")

        if self.printer.is_kernel_driver_active(0):
            try:
                self.printer.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print("Could not detatch kernel driver: %s" % str(e))

        try:
            self.printer.set_configuration()
            self.printer.reset()
        except usb.core.USBError as e:
            print("Could not set configuration: %s" % str(e))

    def write_bytes(self, byte_array):
        msg = ''.join([chr(b) for b in byte_array])
        self.printer.write(self.out_ep, msg, self.interface)

    # Feeds by the specified number of lines
    def linefeed(self, lines = 1):
        if lines == 1:
            self.write_bytes([10]) # LF
        else:
            self.write_bytes([
                27,     # ESC
                100,    # d
                lines])

    def print_text(self, msg):
        self.printer.write(self.out_ep, msg, self.interface)

    # Full paper cut
    def cut(self):
        byte_array = [
            29, # GS
            86, # V
            0]  # \0
        self.write_bytes(byte_array)

    # Print bitmap pixel array for the specified image width and image height
    # To convert an existing image to a 1 and 0 bitmap array, see util.BitmapData
    def print_bitmap(self, pixels, w, h):

        byte_array = []

        dyl = 2 * h % 256
        dyh = int(2 * h / 256)

        # Set the size of the print area
        byte_array.extend([
            27,    # ESC
            87,    # W
            46,     # xL
            0,     # xH
            0,     # yL
            0,     # yH
            0,     # dxL
            2,     # dxH
            dyl,
            dyh])

        # Enter page mode
        byte_array.extend([
            27,
            76])


        # Calculate nL and nH
        nh = int(w / 256)
        nl = w % 256

        offset = 0

        while offset < h:
            byte_array.extend([
                27,  # ESC
                42,  # *
                33,  # double density mode
                nl,
                nh])

            for x in range(w):
                for k in range(3):
                    slice = 0
                    for b in range(8):
                        y = offset + (k * 8) + b
                        i = (y * w) + x
                        v = 0
                        if i < len(pixels):
                            v = pixels[i]
                        slice |= (v << (7 - b))

                    byte_array.append(slice)

            offset += 24

            byte_array.extend([
                27,   # ESC
                74,   # J
                48])

        # Return to standard mode
        byte_array.append(12)

        self.write_bytes(byte_array)

    # n = 0     1-dot-width
    # n =1      2-dots-width
    def underline_on(self, weight = 1):
        byte_array = [
            27,    # ESC
            45,    # -
            weight]
        self.write_bytes(byte_array)

    def underline_off(self):
        byte_array = [
            27,    # ESC
            45,    # -
            0]
        self.write_bytes(byte_array)

    def bold_on(self):
        byte_array = [
            27,     # ESC
            69,      # E
            1]
        self.write_bytes(byte_array)

    def bold_off(self):
        byte_array = [
            27,     # ESC
            69,      # E
            0]
        self.write_bytes(byte_array)

    # Set line spacing with a given number of dots. Default is 30
    def set_line_spacing(self, dots):
        byte_array = [
            27,  # ESC
            51,  # 3
            dots]
        self.write_bytes(byte_array)

    def set_default_line_spacing(self):
        byte_array = [
            27,   # ESC
            50]   #2
        self.write_bytes(byte_array)

    # Set the text size. width_magnification and height_magnification can be between 0(x1) and 7(x8)
    def set_text_size(self, width_magnification, height_magnification):
        if width_magnification < 0 or width_magnification > 7:
            raise Exception("Width magnification should be between 0(x1) and 7(x8)")
        if height_magnification < 0 or height_magnification > 7:
            raise Exception("Height magnification should be between 0(x1) and 7(x8)")
        n = 16 * width_magnification + height_magnification
        byte_array = [
            29,   #GS
            33,   #!
            n]
        self.write_bytes(byte_array)

    def center(self):
        byte_array = [
            27,   # ESC
            97,    # a
            1]
        self.write_bytes(byte_array)

    def left_justified(self):
        byte_array = [
            27,   # ESC
            97,    # a
            0]
        self.write_bytes(byte_array)

    def right_justified(self):
        byte_array = [
            27,   # ESC
            97,    # a
            2]
        self.write_bytes(byte_array)



