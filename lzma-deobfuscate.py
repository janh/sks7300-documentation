#!/usr/bin/env python

import sys
import os
import struct


magic = [
  0x92, 0x47, 0x43, 0x2e, 0x93, 0x48, 0x13, 0x6b,
  0xcc, 0x18, 0x26, 0x6a, 0xc6, 0x1e, 0x52, 0x35,
  0x9e, 0x03, 0x47, 0x36, 0xc6, 0x1e, 0x26, 0x69,
  0xc6, 0x7a, 0x17, 0x67, 0xc0, 0x1b, 0x4e, 0x2e,
  0xc6, 0x25, 0x45, 0x35, 0x93, 0x57, 0x4e, 0x2e,
  0x82, 0x8b, 0x26, 0x4c, 0x9e, 0x08, 0x42, 0x3e,
  0x9a, 0x40, 0x16, 0x6a, 0xc0, 0x4e, 0x1c, 0x6a,
  0x99, 0x4c, 0x16, 0x60, 0x94, 0x40, 0x13, 0x3b,
]

magic1 = magic[0:8]
magic3 = magic[8:16]
magic5 = magic[16:24]
magic7 = magic[24:32]
magic9 = magic[32:40]
magic11 = magic[40:48]
magic13 = magic[48:56]
magic15 = magic[56:64]


def convert_header(header):
	if header[0] != 0x5e or header[1] != 0x71:
		raise Exception('Invalid magic values in first two bytes')

	values = struct.unpack('>BBBBBxBBBBI', header[2:])
	special1, special2, pb, lp, lc, ds2, ds3, ds4, ds1, size = values

	special = (special1 + special2) & 0xf

	pb ^= 0x37
	lp ^= 0x5e
	lc ^= 0xb9

	dicSize = ds1 << 24 | ds2 << 16 | ds3 << 8 | ds4

	props = (pb * 5 + lp) * 9 + lc

	new_header = struct.pack('<BIQ', props, dicSize, size)

	return new_header, special


def convert_compressed(data, special):
	pos = 0
	while pos < len(data):
		for i in range(0, 8):
			index = pos + i
			if index >= len(data):
				return

			old = data[index]

			if special == 0:
				data[index] = ((i + 0x50) & 0xff) ^ data[index]
			elif special == 1:
				data[index] = data[index] ^ magic1[i]
			elif special == 2:
				data[index] = i ^ data[index]
			elif special == 3:
				data[index] = data[index] ^ magic3[i]
			elif special == 4:
				data[index] = ((i + 0x20) & 0xff) ^ data[index]
			elif special == 5:
				data[index] = data[index] ^ magic5[i]
			elif special == 6:
				data[index] = ((i + 0x24) & 0xff) ^ data[index]
			elif special == 7:
				data[index] = data[index] ^ magic7[i]
			elif special == 8:
				data[index] = ((i + 0x84) & 0xff) ^ data[index]
			elif special == 9:
				data[index] = data[index] ^ magic9[i]
			elif special == 10:
				data[index] = ((i - 3) & 0xff) ^ data[index]
			elif special == 11:
				data[index] = data[index] ^ magic11[i]
			elif special == 12:
				data[index] = ((i + 0x3d) & 0xff) ^ data[index]
			elif special == 13:
				data[index] = data[index] ^ magic13[i]
			elif special == 14:
				data[index] = ((i + 0x6a) & 0xff) ^ data[index]
			elif special == 15:
				data[index] = data[index] ^ magic15[i]

		pos += 0x4000


if __name__ == '__main__':
	file_in = sys.argv[1]
	file_out = sys.argv[2]

	with open(file_in, 'rb') as f:
    		data = f.read()

	header = data[0:16]
	compressed = bytearray(data[16:])

	new_header, special = convert_header(header)
	convert_compressed(compressed, special)

	with open(file_out, 'wb') as f:
		f.write(new_header)
		f.write(compressed)
