# UniXNU-pyxis

UniXNU Darwin / XNU bringup repository for **Xiaomi Mi 9 Lite (`pyxis`)** powered by Qualcomm Snapdragon 710 (`SDM710`).

## Target Hardware Specifications

* **Device**: Xiaomi Mi 9 Lite (`pyxis`)
* **SoC**: Qualcomm Snapdragon 710 (`SDM710` / `SDM670` platform family)
* **Architecture**: ARMv8.0-A (Kryo 360: 2x Cortex-A75 @ 2.2 GHz, 6x Cortex-A55 @ 1.7 GHz)
* **GPU**: Qualcomm Adreno 616
* **Memory**: 6 GB LPDDR4X (`0x180000000` @ base `0x80000000`)
* **Interrupt Controller**: ARM GICv3 (`0x17A00000`)
* **Debug UART**: Qualcomm QUPv3 GENI SE (`0x008C0000`)

## Repository Structure

* `board.toml` — UniXNU board and bootloader specification.
* `dts/` — Extracted and decompiled device trees from hardware (`pyxis.dtb`, `pyxis.dts`).
* `configs/` — Kernel defconfigs and target configuration fragments.
* `patches/` — Hardware-specific XNU kernel patches.
* `scripts/` — Porting, packaging, and validation utilities.

## References

* Core UniXNU Framework: https://github.com/UniXNU/UniXNU
* Device Tree Source: https://github.com/qliazar/android_kernel_xiaomi_sdm710
