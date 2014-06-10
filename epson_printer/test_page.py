from Epson_Thermal import Epson_Thermal
from util import BitmapData
from optparse import OptionParser

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-v", "--idvendor", action="store", type="int", dest="id_vendor", help="The printer vendor id")
    parser.add_option("-p", "--idProduct", action="store", type="int", dest="id_product", help="The printer product id")
    options, args = parser.parse_args()
    if (options.id_vendor == None or options.id_vendor == None):
        parser.print_help()
    else:
        printer = Epson_Thermal(options.id_vendor, options.id_product)
        printer.print_text("Hello, how's it going?")
        printer.linefeed()
        printer.print_text("Part of this")
        printer.bold_on()
        printer.print_text(" line is bold")
        printer.bold_off()
        printer.linefeed()
        printer.underline_on()
        printer.print_text("Underlined")
        printer.underline_off()
        printer.linefeed()
        printer.right_justified()
        printer.print_text("Right justified")
        printer.linefeed()
        printer.center()
        printer.print_text("Center justified")
        printer.linefeed()
        printer.left_justified()
        printer.print_text("Left justified")
        printer.linefeed()
        printer.set_text_size(1, 1)
        printer.print_text("Double size text")
        printer.set_text_size(0, 0)
        printer.linefeed()
        printer.print_text("Following is a bitmap")
        printer.linefeed()
        bitmap = BitmapData.fromFileImage("logo.png")
        printer.print_bitmap(bitmap.pixels, bitmap.width, bitmap.height)
        printer.linefeed(4)
        printer.cut()