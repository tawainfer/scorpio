import os
import sys
import pathlib
import subprocess
from tkinter import filedialog

def export_drawio(path, type):
  if type not in ['jpeg', 'jpg', 'png', 'svg', 'xml']:
    return

  base = str(path)
  while not base.endswith('.') and len(base) > 0:
    base = base[:len(base) - 1]

  cmd = f"draw.io -xf {type} -o '{base}{type}' '{base}drawio'"
  try:
    result = subprocess.run(cmd, shell = True, check = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(result.stdout.decode())
  except subprocess.CalledProcessError as e:
    print(e.stdout.decode())
    print(e.stderr.decode())

if __name__ == '__main__':
  script_dir = os.path.dirname(os.path.abspath(__file__))
  os.chdir(script_dir)

  dir_path = filedialog.askdirectory()
  if not dir_path:
    sys.exit()

  p = pathlib.Path(dir_path)
  for path in p.glob("**/*.drawio"):
    export_drawio(path, 'png')
