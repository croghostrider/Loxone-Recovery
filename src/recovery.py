#!/usr/bin/env python3
"""
The methods for unpacking the sps0.LoxCC.

I have tried to add as much documentation as possible
to keep it understandable. its basen on this script:
https://github.com/sarnau/Inside-The-Loxone-Miniserver/blob/master/Code/loadMiniserverConfigurationFile.py
"""

import struct
import zipfile
import zlib


def lox_backup(filename, source, destination):
    """Generate a manifest from a legacy module."""
    zf = zipfile.ZipFile(f"{source}/{filename}")
    with zf.open("sps0.LoxCC") as f:
        (header,) = struct.unpack("<L", f.read(4))
        if header == 0xAABBCCEE:  # magic word to detect a compressed file
            create_backup_file(f, filename, destination)


def create_backup_file(f, filename, destination):
    (
        compressedSize,
        uncompressedSize,
        checksum,
    ) = struct.unpack("<LLL", f.read(12))
    data = f.read(compressedSize)
    index = 0
    resultStr = bytearray()
    while index < len(data):
        # the first byte contains the number of bytes to copy in the upper
        # nibble. If this nibble is 15, then another byte follows with
        # the remainder of bytes to copy. (Comment: it might be possible that
        # it follows the same scheme as below, which means: if more than
        # 255+15 bytes need to be copied, another 0xff byte follows and so on)
        (byte,) = struct.unpack("<B", data[index : index + 1])
        index += 1
        copyBytes = byte >> 4
        byte &= 0xF
        if copyBytes == 15:
            while True:
                addByte = data[index]
                copyBytes += addByte
                index += 1
                if addByte != 0xFF:
                    break
        if copyBytes > 0:
            resultStr += data[index : index + copyBytes]
            index += copyBytes
        if index >= len(data):
            break
        # Reference to data which already was copied into the result.
        # bytesBack is the offset from the end of the string
        (bytesBack,) = struct.unpack("<H", data[index : index + 2])
        index += 2
        # the number of bytes to be transferred is at least 4 plus the lower
        # nibble of the package header.
        bytesBackCopied = 4 + byte
        if byte == 15:
            # if the header was 15, then more than 19 bytes need to be copied.
            while True:
                (val,) = struct.unpack("<B", data[index : index + 1])
                bytesBackCopied += val
                index += 1
                if val != 0xFF:
                    break
                # Duplicating the last byte in the buffer multiple times is possible,
                # so we need to account for that.
        while bytesBackCopied > 0:
            resultStr += resultStr[-bytesBack:] if -bytesBack == -1 else resultStr[-bytesBack : -bytesBack + 1]

            bytesBackCopied -= 1
    if checksum != zlib.crc32(resultStr):
        print("Checksum is wrong")
        exit(1)
    if len(resultStr) != uncompressedSize:
        print(
            "Uncompressed filesize is wrong %d != %d"
            % (len(resultStr), uncompressedSize)
        )
        exit(1)
    newfilename = (
        filename[:13]
        + "-"
        + filename[13:][:2]
        + "-"
        + filename[15:][:2]
        + "-"
        + filename[17:][:6]
    )
    print(newfilename)
    with open(f"{destination}/{newfilename}.Loxone", "wb") as f:
        f.write(resultStr)
