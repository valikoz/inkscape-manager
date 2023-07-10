import os
import subprocess
from pathlib import Path


def picker(dir): 
    '''Called fzf which search files in specified directory.

    :param dir: Directory where fzf will search files.
    :returns: Location of the selected file.
    :rtype: str
    '''
    ROOT_DIR = Path(__file__).parent.parent
    OUTPUT_FILE = os.path.join(ROOT_DIR, 'stdout.txt') 
    cmd = f"start /wait cmd /c \"fd . {dir} | fzf --query .svg$ >{OUTPUT_FILE}\""
    subprocess.run(cmd, shell=True)
    # Open the file contained path to the selected file.
    with open(OUTPUT_FILE, 'r+') as stdout:
        path = stdout.read().strip()
        stdout.write('')
    return path
