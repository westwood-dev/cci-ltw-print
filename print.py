#
# Conda environment: ltw-print
# Python version: 3.11.11
#

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

setting = {
  "serial_com_port": "COM4",
  "line_char_length": 42,
  "image_size": 512,
}

bodyText = "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."

def format_text(text, width=setting['line_char_length']):
  """Formats the input text to fit within a specified width, wrapping lines as necessary. Only where spaces exist."""
  words = text.split()
  formatted_lines = []
  current_line = ""

  for word in words:
    if len(current_line) + len(word) + 1 <= width:
      if current_line:
        current_line += " "
      current_line += word
    else:
      formatted_lines.append(current_line)
      current_line = word

  if current_line:
    formatted_lines.append(current_line)

  return "\n".join(formatted_lines)

def printProfileDev(data):
    print('')
    print('------------------------------------------')
    print('')
    print('UAL LOGO')
    print('')
    print('------------------------------------------')
    print('')
    print('MAIN IMAGE:', data.main.size)
    print('SECOND IMAGE:', data.second.size)
    print('timestamp:', data.timestamp)
    print('Title of work:', data.title)
    print('BodyText:', format_text(bodyText))
    print('')
    print('------------------------------------------')
    print('')
    print('------------------------------------------')
    print('')

    # data.main.show()
    # data.second.show()


def printProfile(data):
    # print(get_profile('TM-T88III').profile_data)

    p = printer.Serial(devfile=setting['serial_com_port'],
              baudrate=38400,
              bytesize=8,
              parity='N',
              stopbits=1,
              timeout=1.00,
              dsrdtr=True,
              profile="TM-T88III")
    
    p.image('.\\assets\\images\\ual-cci-logo.png')
    p.text('\n')
    if len(data.main) > 0:
      p.image(data.main)
    p.text('\n')
    if len(data.second) > 0:
      p.image(data.second)
    p.text('\n')
    p.set(align='center')
    p.textln(data.timestamp)
    p.text('\n')
    p.set(bold=True)
    p.textln(data.title)
    p.text('\n')
    p.set(bold=False, align='left')
    p.text(format_text(bodyText)+'\n')
    p.set(align='center')
    p.qr('https://www.arts.ac.uk/ual', center=True, size=16)
    
    p.cut()


def resize_and_rotate_image(image):

    max = setting['image_size']

    if image.size[0] > image.size[1]:
        image = image.rotate(90, expand=True)
    
    image = image.resize((max, int(max * image.size[1] / image.size[0])), Image.Resampling.BICUBIC)
    return image


def load_user_data_from_json(json_data):

  data = json.loads(json_data, object_hook=lambda d: SimpleNamespace(**d))
  
  if hasattr(data, 'images_base64'):
    for i in range(len(data.images_base64)):
      base64_string = data.images_base64[i]
      if "data:image" in base64_string:
        base64_string = base64_string.split(",")[1]
      image_bytes = base64.b64decode(base64_string)
      data.images.append(resize_and_rotate_image(Image.open(io.BytesIO(image_bytes))))

  if hasattr(data, 'main') and len(data.main) > 0:
    base64_string = data.main
    if "data:image" in base64_string:
      base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)
    data.main = resize_and_rotate_image(Image.open(io.BytesIO(image_bytes)))

  if hasattr(data, 'second') and len(data.second) > 0:
    base64_string = data.second
    if "data:image" in base64_string:
      base64_string = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_string)
    data.second = resize_and_rotate_image(Image.open(io.BytesIO(image_bytes)))

  return data

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Print profile from JSON data')
  parser.add_argument('--json', type=str, help='JSON data as string')
  parser.add_argument('--file', type=str, help='Path to JSON file')
  args = parser.parse_args()
  
  if args.json:
    json_data = args.json
  elif args.file:
    with open(args.file, 'r') as f:
      json_data = f.read()
  else:
    if not sys.stdin.isatty():
      json_data = sys.stdin.read()
    else:
      print("Error: No JSON data provided. Use --json, --file, or pipe data in.")
      sys.exit(1)
  
  user_data = load_user_data_from_json(json_data)
  
  printProfile(user_data)