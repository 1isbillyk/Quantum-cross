#!/usr/bin/env python3
import sys
import binascii
import os


def printProgressBar(progress):
    i = int(progress * 20)
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    sys.stdout.flush()

def openFileToByte_generator(filename , chunkSize = 128):
    fileSize = os.stat(filename).st_size
    readBytes = 0.0
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunkSize)
            readBytes += chunkSize
            printProgressBar(readBytes/float(fileSize))
            if chunk:
                for byte in chunk:
                    yield byte.to_bytes(1, byteorder='big')
            else:
                break


if(len(sys.argv) != 3):
	sys.exit('usage: binConverter.py "pathToFile\\fileName.bin payloadX"')

fileIn = sys.argv[1]
payloadNum = str(sys.argv[2]).lower()


base = os.path.splitext(fileIn)[0]
fileOut =  payloadNum + ".h"

stringBuffer = "\t"
countBytes = 0
print("reading file: " + fileIn)

for byte in openFileToByte_generator(fileIn,16):
    countBytes += 1
    stringBuffer += "0x"+binascii.hexlify(byte).decode('ascii')+", "
    if countBytes%16 == 0:
    	stringBuffer += "\n\t"



stringBuffer = f"#include <Arduino.h>\n" \
               f"//{fileIn}\n" \
               f"#define {payloadNum.upper()}_SIZE {countBytes}\n" \
               f"const PROGMEM byte {payloadNum}Bin[{payloadNum.upper()}_SIZE] =" + " {\n" \
               f"{stringBuffer}\n" \
               "};"

print("\nwriting file: " + fileOut)
text_file = open(fileOut, "w")
text_file.write(stringBuffer)
text_file.close()

print("finished")
