import sys
from cx_Freeze import setup, Executable

setup(
    name = "Longclaw",
    version = "1.0",
    description = "Longclaw is a Photo enhance and photo editing tool developed by Rishabh Jain and Rishabh Kumar.",
    executables = [Executable("yourFileName.py", base = "Win32GUI")])
