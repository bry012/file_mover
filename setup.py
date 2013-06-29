################################################
# A simply setup script for creating an executable
# python app using cx_freeze
# otengkwaku@gmail.com
################################################

import sys
from cx_Freeze import setup, Executable

includes = ['atexit']
packages = ['Tkinter', 'tkFileDialog','sqlite3','shutil']
base = None
if sys.platform == 'win32':
    base = 'Win32Gui'

setup(
    #icon = 'editpaste.png',

    name = 'File_mover',
    version= '0.8',
    description = 'A python program the easily moves muliple\
                    selected file types from and to diretories of choice',
    options = {'build_exe':{'includes':includes, 'packages':packages}},
    executables = [Executable("Freeze_file_mover.py",base = base)]
    )
    
