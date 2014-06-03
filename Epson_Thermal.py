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
        bytes = [
            chr(29), # GS
            chr(86), # V
            chr(0)]  # \0
        command = ''.join(bytes)
        self._write(command)

    # def print_bitmap(self, pixels, w, h):


if __name__ == '__main__':
    printer = Epson_Thermal(0x04b8,0x0e03)  # EPSON TM-T20
    printer.print_text("Hello world")
    printer.linefeed()
    printer.cut()
