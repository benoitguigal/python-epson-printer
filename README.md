Python library for EPSON thermal printers
====================

A python library to control thermal printers based on the ESC/POS language as defined by Epson.

### Devices
The library should work with all ESC/POS-based Epson printers but it has only been tested with a TM-T20.

### ESC/POS commands

##### Print commands
* print text
* feed lines

##### Character commands
* Left, right or centered justified
* Bold ON/OFF
* Underline ON/OFF
* Font size

##### Bit image commands
* print arbitrary long bitmap pixels array

##### Hardware commands
* full paper cut


### Credits
* [python-escpos code on google](https://code.google.com/p/python-escpos/)
* [sending-a-bit-image-to-an-epson-tm-t88iii-receipt-printer-using-c-and-escpos blog post](http://nicholas.piasecki.name/blog/2009/12/sending-a-bit-image-to-an-epson-tm-t88iii-receipt-printer-using-c-and-escpos/)

