from cx_Freeze import setup, Executable

base = None

executables = [Executable("gui.py", base=base)]

packages = ["kivy", "pylibdmtx", "pytesseract", "PIL", "numpy"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name = "Check Scanner",
    options = options,
    version = "1.0",
    description = 'An application to read and compare QR and MICR codes on checks',
    executables = executables
)
