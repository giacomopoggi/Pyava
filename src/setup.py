from cx_Freeze import setup, Executable
import os
import sys

os.environ["TCL_LIBRARY"] = r"C:\Python36-32\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\Python36-32\tcl\tk8.6"

buildOptions = dict(
    packages=[],
    excludes=[],
    include_files=[
        r"C:\Python36-32\DLLs\tcl86t.dll",
        r"C:\Python36-32\DLLs\tk86t.dll",
        r"pyava\icon.ico",
        r"pyava\config.ini"
    ]
)

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        r"pyava\pyava.py",
        base=base,
        icon=r"pyava\icon.ico"
    )
]

setup(
    name="Pyava",
    version="1.0",
    description="A simple emulator launcher written in Python.",
    options=dict(build_exe=buildOptions),
    executables=executables
)
