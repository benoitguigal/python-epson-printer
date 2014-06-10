__author__ = 'benoit'

from setuptools import setup

setup(name="python_epson_printer",
      version="1.0",
      description="A library to control Epson thermal printers based on ESC/POS language",
      url="https://github.com/benoitguigal/python-epson-printer",
      author="benoitguigal",
      author_email="benoit.guigal@gmail.com",
      packages=['epson_printer'],
      install_requires=[
          'pyusb',
          'Pillow'
      ])
