#!/usr/bin/env python3
"""Pack a sparse root disk / APFS image into DarwinBoot DBRDISK1 format.

Reference format: DarwinBoot/DarwinBootPkg/Driver/PackedRamdisk.h
Magic: "DBRDISK1", Version: 1, PageSize: 4096
"""
import sys, os, struct, argparse

PAGE_SIZE = 4096

def pack_file_to_dbrdisk(input_path, output_path):
    if not os.path.exists(input_path):
        sys.exit(f"Input file not found: {input_path}")
    
    file_size = os.path.getsize(input_path)
    logical_size = (file_size + PAGE_SIZE - 1) & ~(PAGE_SIZE - 1)

    print(f"Packing {input_path} (size={file_size}, aligned={logical_size})...")

    extents = []
    with open(input_path, "rb") as f:
        offset = 0
        while True:
            chunk = f.read(PAGE_SIZE * 64) # 256KB chunks
            if not chunk:
                break
            # Skip zero blocks
            if any(chunk):
                extents.append((offset, chunk))
            offset += len(chunk)

    if not extents:
        extents = [(0, b'\x00' * PAGE_SIZE)]

    magic = b"DBRDISK1"
    version = 1
    count = len(extents)
    header = struct.pack("<8sIIQQ", magic, version, PAGE_SIZE, logical_size, count)

    table = b""
    payload = b""
    for off, data in extents:
        # Pad data to PAGE_SIZE if needed
        if len(data) % PAGE_SIZE != 0:
            pad = PAGE_SIZE - (len(data) % PAGE_SIZE)
            data += b'\x00' * pad
        table += struct.pack("<QQ", off, len(data))
        payload += data

    packed_data = header + table + payload
    with open(output_path, "wb") as out:
        out.write(packed_data)

    print(f"Created {output_path}: {len(packed_data)} bytes ({len(extents)} non-zero extents)")

def main():
    parser = argparse.ArgumentParser(description="DarwinBoot DBRDISK1 ramdisk packer")
    parser.add_argument("input", help="Source disk image")
    parser.add_argument("-o", "--output", default="ramdisk.packed", help="Output packed file")
    args = parser.parse_args()

    pack_file_to_dbrdisk(args.input, args.output)

if __name__ == "__main__":
    main()
