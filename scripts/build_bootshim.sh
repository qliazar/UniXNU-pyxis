#!/bin/bash
set -e

UEFI_BASE="0x9FC00000"
UEFI_SIZE="0x00300000"

echo "=== Compiling BootShim for SDM710 (Base: $UEFI_BASE, Size: $UEFI_SIZE) ==="
mkdir -p build/shim

aarch64-linux-gnu-gcc \
  -DUEFI_BASE=$UEFI_BASE \
  -DUEFI_SIZE=$UEFI_SIZE \
  -Werror -Wall \
  -fpie \
  -c firmware/BootShim/BootShim.S \
  -o build/shim/BootShim.o

aarch64-linux-gnu-ld \
  -Ttext 0x80008000 \
  -o build/shim/BootShim.elf \
  build/shim/BootShim.o

aarch64-linux-gnu-objcopy \
  -O binary \
  -j .text \
  build/shim/BootShim.elf \
  build/shim/BootShim.bin

ls -lh build/shim/BootShim.bin
