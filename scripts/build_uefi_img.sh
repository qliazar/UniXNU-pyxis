#!/bin/bash
set -e

echo "=== Assembling uefi.img for Mi 9 Lite (SDM710) ==="
mkdir -p out/firmware

# Download AOSP mkbootimg
curl -sL -o /tmp/mkbootimg.py https://raw.githubusercontent.com/aosp-mirror/platform_system_tools_mkbootimg/master/mkbootimg.py

# Bundle DTB and payload
cat dts/pyxis.dtb > out/firmware/uefi-kernel-payload.bin
gzip -c out/firmware/uefi-kernel-payload.bin > out/firmware/uefi-payload.gz
touch /tmp/empty-ramdisk.cpio

# Assemble boot.img
python3 /tmp/mkbootimg.py \
  --kernel out/firmware/uefi-payload.gz \
  --ramdisk /tmp/empty-ramdisk.cpio \
  --base 0x80000000 \
  --kernel_offset 0x00008000 \
  --ramdisk_offset 0x01000000 \
  --tags_offset 0x00000100 \
  --pagesize 4096 \
  --cmdline "console=ttyMSM0,115200n8 earlycon=msm_geni_serial,0x8c0000" \
  --header_version 1 \
  -o out/uefi.img

ls -lh out/uefi.img
