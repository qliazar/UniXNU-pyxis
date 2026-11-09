#!/usr/bin/env python3
"""Standalone Android boot.img v1 packer (AOSP compatible) for Pyxis (SDM710)."""
import sys, os, struct, argparse

BOOT_MAGIC = b'ANDROID!'

def pad_file(f, page_size):
    pad = (page_size - (f.tell() % page_size)) % page_size
    f.write(b'\x00' * pad)

def main():
    parser = argparse.ArgumentParser(description="Standalone Android boot.img packer")
    parser.add_argument("--kernel", required=True, help="Kernel binary")
    parser.add_argument("--ramdisk", default=None, help="Ramdisk image")
    parser.add_argument("--base", default="0x80000000", help="Base address")
    parser.add_argument("--kernel_offset", default="0x00008000", help="Kernel offset")
    parser.add_argument("--ramdisk_offset", default="0x01000000", help="Ramdisk offset")
    parser.add_argument("--tags_offset", default="0x00000100", help="Tags offset")
    parser.add_argument("--pagesize", type=int, default=4096, help="Page size")
    parser.add_argument("--header_version", type=int, default=1, help="Header version")
    parser.add_argument("--cmdline", default="", help="Kernel command line")
    parser.add_argument("-o", "--output", required=True, help="Output image")
    args = parser.parse_args()

    base = int(args.base, 16)
    kernel_addr = base + int(args.kernel_offset, 16)
    ramdisk_addr = base + int(args.ramdisk_offset, 16)
    tags_addr = base + int(args.tags_offset, 16)

    kernel_data = open(args.kernel, 'rb').read()
    ramdisk_data = open(args.ramdisk, 'rb').read() if args.ramdisk and os.path.exists(args.ramdisk) else b''

    kernel_size = len(kernel_data)
    ramdisk_size = len(ramdisk_data)
    second_size = 0
    second_addr = 0
    cmdline = args.cmdline.encode('utf-8')[:512].ljust(512, b'\x00')
    name = b'UniXNU-Pyxis'.ljust(16, b'\x00')
    extra_cmdline = b''.ljust(1024, b'\x00')
    header_version = args.header_version
    os_version = 0

    # Header v1 format (1648 bytes)
    header = struct.pack(
        '<8sIIIIIIIIII16s512s1024s',
        BOOT_MAGIC,
        kernel_size, kernel_addr,
        ramdisk_size, ramdisk_addr,
        second_size, second_addr,
        tags_addr, args.pagesize,
        header_version, os_version,
        name, cmdline,
        extra_cmdline
    )
    # v1 fields
    recovery_dtbo_size = 0
    recovery_dtbo_offset = 0
    header_size = 1648
    v1_tail = struct.pack('<IQI', recovery_dtbo_size, recovery_dtbo_offset, header_size)

    with open(args.output, 'wb') as out:
        out.write(header + v1_tail)
        pad_file(out, args.pagesize)
        out.write(kernel_data)
        pad_file(out, args.pagesize)
        if ramdisk_size > 0:
            out.write(ramdisk_data)
            pad_file(out, args.pagesize)

    print(f"Created {args.output}: {os.path.getsize(args.output)} bytes (kernel={kernel_size}, ramdisk={ramdisk_size})")

if __name__ == '__main__':
    main()
