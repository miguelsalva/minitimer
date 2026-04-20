# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for minitimer
# Build: pyinstaller minitimer.spec

block_cipher = None

a = Analysis(
    ['minitimer_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('images/tomato.png',   'images'),
        ('images/minitimer.icns', 'images'),
        ('vinyl-piano_100bpm_C_minor.mp3', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='minitimer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='images/minitimer.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='minitimer',
)

app = BUNDLE(
    coll,
    name='minitimer.app',
    icon='images/minitimer.icns',
    bundle_identifier='com.miguelsalva.minitimer',
    info_plist={
        'NSHighResolutionCapable': True,
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleName': 'minitimer',
        'LSUIElement': False,
    },
)
