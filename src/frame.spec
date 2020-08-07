# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['frame.py'],
             pathex=['C:\\Users\\Administator\\Desktop\\sample\\src'],
             binaries=[],
             datas=[('libiconv.dll','.'), ('libzbar-64.dll','.'), ('opencv_videoio_ffmpeg430_64.dll', '.'),('power-tiny.cfg','.'), ('power-tiny_20000.weights','.')],
             hiddenimports=['pyzbar'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='frame',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='frame')
