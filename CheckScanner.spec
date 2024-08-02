# CheckScanner.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=['.'],
    binaries=[
        (r'C:\Users\alios\PycharmProjects\Cheque-Reader\.venv\Lib\site-packages\pylibdmtx\libdmtx-64.dll', '.')  # libdmtx-64.dll dosyasını ekleyin
    ],
    datas=[
        (r'C:\Users\alios\PycharmProjects\Cheque-Reader\qr_reader.py', '.'),
        (r'C:\Users\alios\PycharmProjects\Cheque-Reader\micr_reader.py', '.'),
        (r'C:\Program Files\Tesseract-OCR\tesseract.exe', '.'),
        (r'C:\Program Files\Tesseract-OCR\tessdata', 'tessdata'),
        (r'C:\Users\alios\PycharmProjects\Cheque-Reader\resources\icon.webq', 'resources'),
        (r'C:\Users\alios\PycharmProjects\Cheque-Reader\resources\ornek_cek.png', 'resources')  # ornek_cek.png dosyasını ekleyin
    ],
    hiddenimports=[
        'kivy.deps.sdl2',
        'kivy.deps.glew',
        'kivy.deps.gstreamer'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CheckScanner',
    icon='resources/icon.webq',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CheckScanner',
)
