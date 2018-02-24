from sys import argv
import mmap


def copy_file(filepath):
	with open(filepath, "rb") as f:
		open("glitch.jpg", "wb").write(f.read())


def encode_in_image(message):
	with open("glitch.jpg", "r+b") as f:
		raw = f.read()
		locations = {}
		index = 1000;
		skip = round((len(raw) - index) / (len(message)*0.9))
		# print("skip is [{}]".format(skip))
		for iterator in range(0, len(message)):
			index = 1000 + (iterator*skip)
			character = message[iterator]
			locations[index] = character.encode()
		# print("created location index")
		mm = mmap.mmap(f.fileno(), 0)
		for key in locations:
			current = key
			# print("seeking [{}]".format(current))
			if key > mm.size():
				current = (-1 * mm.size()) + key
				# print("overflow, setting new key to [{}]".format(current))
			mm.seek(current)
			# print("writing [{}] at [{}]".format(locations[key][0], current))
			mm.write_byte(locations[key][0])
		mm.seek(mm.size()-1)
		mm.write_byte(len(message))
		mm.close()


def decode_from_image(filepath):
	with open(filepath, "r+b") as f:
		mm = mmap.mmap(f.fileno(), 0)
		mm.seek(mm.size()-1)
		nchars = mm.read_byte()
		raw = f.read()
		locations = []
		final = ""
		index = 1000;
		skip = round((len(raw) - index) / (nchars*0.9))
		# print("skip is [{}]".format(skip))
		for iterator in range(0, nchars):
			index = 1000 + (iterator*skip)
			locations.append(index)
		# print("created location index")
		for key in locations:
			current = key
			# print("seeking [{}]".format(current))
			if key > mm.size():
				current = (-1 * mm.size()) + key
				# print("overflow, setting new key to [{}]".format(current))
			mm.seek(current)
			final += chr(mm.read_byte())
		print(final)
		mm.close()


# decoding

usage = """
decoding: python glitxt.py decode [filepath]
encoding: python glitxt.py encode [filename] [message (no spaces)]
"""

if len(argv) == 3 and argv[1] == "decode":
	print("decoding...")
	decode_from_image(argv[2])
elif len(argv) == 4 and argv[1] == "encode":
	print("encoding...")
	copy_file(argv[2])
	encode_in_image(argv[3])
else:
	print(usage)