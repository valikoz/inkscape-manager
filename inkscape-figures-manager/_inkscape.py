import subprocess
from pathlib import Path


def launcher(filepath):
    '''Run command which open a figure in `Inkscape` to edit.

    :param filepath: The file location of the existing figure
    :type filepath: str, Path
    :rtype: <class 'subprocess.Popen'>
    '''
    process = subprocess.Popen(['inkscape', filepath])
    return process


def export_pdf_latex(filepath):
    r'''Run command which export a figure (expected svg format) 
    to pdf and pdf_latex formats.

    :param filepath: The file location of the existing figure
    :type filepath: str, Path

    :returns: a CompletedProcess instance
    '''

    filepath = Path(filepath)
    pdf_path = filepath.parent / (filepath.stem + '.pdf')
    command = [
        'inkscape', filepath,
        '--export-area-drawing',
        '--export-dpi', '300',
        '--export-type=pdf',
        '--export-latex',
        '--export-filename', pdf_path
        ]
    # Recompile the svg file
    subprocess.run(command)
