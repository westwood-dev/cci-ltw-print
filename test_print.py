from PIL import Image
import matplotlib.pyplot as plt
from escpos import *
# from escpos.capabilities import get_profile
import json
import base64
import numpy as np
import argparse
from types import SimpleNamespace
import io
import sys

def printProfile():
    
    p = printer.Serial(devfile=setting['serial_com_port'],
              baudrate=38400,
              bytesize=8,
              parity='N',
              stopbits=1,
              timeout=1.00,
              dsrdtr=True,
              profile="TM-T88III")
    
    p.image('.\\assets\\images\\Future-play-reciept-1.png')
    p.text('\n')
    p.image('.\\assets\\images\\Future-play-reciept-2.png')
    p.text('\n')
    p.image('.\\assets\\images\\Future-play-reciept-3.png')
    p.text('\n')
    p.image('.\\assets\\images\\Future-play-reciept-4.png')
    
    p.set(align='center')
    p.text("\nSize: 6")
    p.qr('https://ualshowcase.arts.ac.uk/collection/future-play', center=True, size=6)
    p.text("\nSize: 8")
    p.qr('https://ualshowcase.arts.ac.uk/collection/future-play', center=True, size=8)
    p.text("\nSize: 10")
    p.qr('https://ualshowcase.arts.ac.uk/collection/future-play', center=True, size=10)
    p.text("\nSize: 12")
    p.qr('https://ualshowcase.arts.ac.uk/collection/future-play', center=True, size=12)
    p.text("\nSize: 14")
    p.qr('https://ualshowcase.arts.ac.uk/collection/future-play', center=True, size=14)
    p.text("\nSize: 16")
    p.qr('https://ualshowcase.arts.ac.uk/collection/future-play', center=True, size=16)
    
    p.cut()

printProfile()
