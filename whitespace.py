#######################################################################################
### Steganography is the technique of hiding secret data within an ordinary medium. ###
#######################################################################################


import sys


commands = {}

def command(func):
    commands[func.__name__] = func
    return func

def getopt(options, shortname, longname, default):
    value = None
    if shortname:
        value = options.get("-" + shortname, None)
    if value: return value
    value = options.get("--" + longname, None)
    if value: return value
    return default


capacity_usage = "whitespace capacity [CODEFILE] [OPTIONS]..."
@command
def capacity(options : dict, *args):
    if len(args) != 1:
        print("Usage:")
        print(capacity_usage)
        exit()
    codepath = args[0]
    
    with open(codepath, "r", encoding="utf8") as f:
        code_lines = f.readlines()
    
    line_count = len(code_lines)
    bits_per_line = int(getopt(options, "b", "bits-per-line", 16))
    bit_capacity = line_count * bits_per_line
    print("This file will fit %d raw bits. (%d bytes)" % (bit_capacity, bit_capacity / 8))


def bytes_to_whitespace(data):
    s = ""
    for byte in data:
        for i in range(8):
            high = byte & 0b10000000
            s += "\t" if high > 0 else " "
            byte <<= 1
    return s

import zlib
embed_usage = "whitespace embed [DATAFILE] [CODEFILE] [OPTIONS]..."
@command
def embed(options : dict, *args):
    if len(args) != 2:
        print("Usage:")
        print(embed_usage)
        exit()
    datapath : str = args[0]
    codepath : str = args[1]

    bits_per_line = int(getopt(options, "b", "bits-per-line", 16))

    raw_data = None
    with open(datapath, "rb") as f:
        raw_data = f.read()
    data = zlib.compress(raw_data)

    code_lines = None
    with open(codepath, "r", encoding="utf8") as f:
        code_lines = f.readlines()

    ext = codepath[(codepath.rfind(".") + 1):]

    data = bytes_to_whitespace(data)

    line_head = 0
    data_head = 0
    while data_head < len(data):
        chunk = data[data_head : (data_head + bits_per_line)]
        line = code_lines[line_head]
        line = line.rstrip()
        for char in chunk:
            line += char
        line += "\n"
        code_lines[line_head] = line

        data_head += bits_per_line
        line_head += 1
        if line_head >= len(code_lines):
            print("Not enough space in target file.")
            print("%d bytes needed." % len(data))
            print("\"%s\" stats:" % codepath)
            capacity(options, codepath)

            exit()
    
    with open("output." + ext, "w", encoding="utf8") as f:
        f.writelines(code_lines)

    

extract_usage = "whitespace extract [CODEFILE] [OPTIONS]..."
@command
def extract(options, *args):
    if len(args) < 1:
        print("Usage:")
        print(extract_usage)
        exit()
    
    codepath : str = args[0]
    code_lines = None
    with open(codepath, "r", encoding="utf8") as f:
        code_lines = f.readlines()
    
    data = ""
    for line in code_lines:
        chunk = line[len(line.rstrip()):-1]
        data += chunk
    
    if len(data) < 8:
        print("File has no whitespace data.")
        exit()

    byte_array = bytearray()
    for i in range(0, len(data), 8):
        byte = 0
        bit = 0b10000000
        for j in range(8):
            char = data[i + j]
            if char == "\t":
                byte += bit
            bit >>= 1
        byte_array.append(byte)
    
    bytes_all = bytes(byte_array)
    bytes_all = zlib.decompress(bytes_all)
    
    with open("output", "wb") as f:
        f.write(bytes_all)


def printHelp():
    print("Usage:")
    print(capacity_usage)
    print(embed_usage)
    print(extract_usage)

    print("Options:")
    print("-b --bits-per-line - (Maximum symbols that can be appended to a line)")
    #print("-o [OUTFILE] - Output file")
    exit()

if len(sys.argv) < 2:
    printHelp()

cmd = commands.get(sys.argv[1])

if not cmd:
    printHelp()

last_option_index = len(sys.argv)
options = {}
for i, arg in enumerate(sys.argv[::-1]):
    if len(sys.argv) <= i + 1:
        continue
    if arg[0] != "-":
        continue
    last_option_index = len(sys.argv) - i - 1
    options[arg] = sys.argv[len(sys.argv) - i]

args = sys.argv[2:last_option_index]
cmd(options, *args)
