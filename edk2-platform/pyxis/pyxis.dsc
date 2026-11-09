[Defines]
  PLATFORM_NAME                  = pyxis
  PLATFORM_GUID                  = 28f1a3bf-193a-47e3-a7b9-5a435eaab2ee
  PLATFORM_VERSION               = 0.1
  DSC_SPECIFICATION              = 0x00010019
  OUTPUT_DIRECTORY               = Build/pyxisPkg
  SUPPORTED_ARCHITECTURES        = AARCH64
  BUILD_TARGETS                  = DEBUG|RELEASE
  SKUID_IDENTIFIER               = DEFAULT
  FLASH_DEFINITION               = edk2-platform/pyxis/pyxis.fdf

[PcdsFixedAtBuild.common]
  # SDM710 Platform Memory Base & Total DRAM Size (6 GB)
  gArmTokenSpaceGuid.PcdSystemMemoryBase|0x80000000
  gArmTokenSpaceGuid.PcdSystemMemorySize|0x180000000

  # Continuous Splash Framebuffer (Mi 9 Lite ABL cont_splash_region @ 0x9C000000)
  gQcomTokenSpaceGuid.PcdMipiFrameBufferAddress|0x9C000000
  gQcomTokenSpaceGuid.PcdMipiFrameBufferWidth|1080
  gQcomTokenSpaceGuid.PcdMipiFrameBufferHeight|2340
  gQcomTokenSpaceGuid.PcdMipiFrameBufferPixelBpp|32

  # GICv3 Configuration for SDM710
  gArmTokenSpaceGuid.PcdGicDistributorBase|0x17A00000
  gArmTokenSpaceGuid.PcdGicRedistributorsBase|0x17A60000

  # CPU Cores (8 cores: 2 Gold + 6 Silver)
  gArmPlatformTokenSpaceGuid.PcdCoreCount|8
  gArmPlatformTokenSpaceGuid.PcdClusterCount|2

  # Serial Console (QUPv3 UART @ 0x008C0000)
  gArmPlatformTokenSpaceGuid.PcdSerialRegisterBase|0x008C0000
