import os
import sys
import pathlib
import subprocess
import xml.etree.ElementTree as et
from tkinter import filedialog

# DRAWIO_PATH = r'draw.io'
DRAWIO_PATH = r'C:\Program Files\draw.io\draw.io.exe'

def export_drawio(path, type):
  if type not in ['jpeg', 'jpg', 'png', 'svg', 'xml']:
    return

  base = str(path)
  while not base.endswith('.') and len(base) > 0:
    base = base[:len(base) - 1]

  cmd = f'"{DRAWIO_PATH}" -xf {type} -o "{base}{type}" "{base}drawio"'
  try:
    subprocess.run(cmd, shell = True, check = True)
  except subprocess.CalledProcessError:
    print(f'failed to execute {cmd}')

def summarize_drawio(path):
  with open(path, 'r', encoding = 'utf-8') as rf:
    data = rf.read()

    root = et.fromstring(data)
    elements = root.findall('.//*[@value]')

    result = list()
    for e in elements:
      child_elements = e.findall('.//*[@as="geometry"]')
      ce = child_elements[0]

      d = dict()
      d['value'] = e.get('value')
      d['x'] = ce.get('x')
      d['y'] = ce.get('y')
      d['width'] = ce.get('width')
      d['height'] = ce.get('height')
      result.append(d)

  with open(f'{path}.summary', 'w', encoding = 'utf-8') as wf:
    for r in result:
      wf.write(str(r) + '\n')

if __name__ == '__main__':
  script_dir = os.path.dirname(os.path.abspath(__file__))
  os.chdir(script_dir)

  dir_path = filedialog.askdirectory()
  if not dir_path:
    sys.exit()

  p = pathlib.Path(dir_path)
  for path in p.glob("**/*.drawio"):
    export_drawio(path, 'png')
    summarize_drawio(path)