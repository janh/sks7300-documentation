# SKS7300

## Bootloader

The bootloader is at the beginning of the flash, starting with the preloader.
The actual U-Boot starts at offset `0x8000` and is loaded at address `0x8ff00000`.

It contains another binary at address `0x8ff1ee20` (size `0x42011`), which is decompressed to `0x8f9f8000` (see below for compression format).
The entry point is at `0x8fa00000`.

## Hidden menu options

The bootloader offers a menu which can be accessed using Ctrl+C.
It is part of the separate binary mentioned above.

There are some hidden menu options which require a password:

- a: `zaq1`
- d: `sw2`
- z: `jiangks`

## Compression

The compression format is based on LZMA with some modifications (probably for obfuscation).

The script `lzma-deobfuscate.py` allows to convert compressed data to the regular LZMA format.
Note that decompression fails if there is any trailing data, so make sure to get the size of the extracted data right.

### Header

The header is 16 bytes long:

- 0-1: magic value: 0x5e 0x71
- 2-3: special value: (header[2] + header[3]) & 0xf
- 4: pb: header[4] ^ 0x37
- 5: lp: header[5] ^ 0x5e
- 6: lc: header[6] ^ 0xb9
- 7: unknown
- 8-11: dictionary size: byte order from most significant to least significant: 11, 8, 10, 9
- 12-15: uncompressed size in big endian

### Compressed data

The first 8 bytes of each 16384 bytes block are modified depending on the special value from the header.
See the included Python script for details.
