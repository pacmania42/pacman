# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

mlx_datas, mlx_binaries, mlx_hidden = collect_all("mlx")

a = Analysis(
    ["pac-man.py"],
    pathex=[],
    binaries=mlx_binaries,
    datas=[("src/assets", "src/assets"), ("config.json", ".")] + mlx_datas,
    hiddenimports=mlx_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="pacman",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=["pacman-icon.ico"],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="pacman",
)
