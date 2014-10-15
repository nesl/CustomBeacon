# -- BLE112 communication constants --
# command class types
CID_SYSTEM = 0x00
CID_PSTORE = 0x01
CID_ATTDB  = 0x02
CID_CNNCT  = 0x03
CID_ATTCL  = 0x04
CID_SMNG   = 0x05
CID_GAP    = 0x06
CID_HW     = 0x07

# selected command types
# system
CMD_HELLO   = 0x01
CMD_GETADDR = 0x02
# hardware
CMD_IODIR   = 0x03
CMD_IOWRITE = 0x06
CMD_IOREAD  = 0x07
CMD_TXPOWER = 0x0C
# GAP
CMD_ADVDATA = 0x09
CMD_ADVPARA = 0x08
CMD_SETMODE = 0x01
