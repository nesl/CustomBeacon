# -- iBeacon Constants --
IBCN_TYPES = bytearray([0x01, 0x1A])
IBCN_PREFIX = bytearray([0xFF, 0x4C, 0x00, 0x02, 0x15])
IBCN_UUID_NESL = bytearray([0x46,0xA7,0x59,0x4F,0x67,0x2D,0x4B,0x6C,0x81,0xC1,0x78,0x5A,0xEC,0xDB,0xA0,0xD5])
IBCN_MAJOR_NESL = 4

# -- CustomBeacon Constants --
CBCN_TYPES = bytearray([0x04])


# -- BLE112 communication constants --
# packet types
TYPE_CMDRESP = 0x00
TYPE_EVENT   = 0x01
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
EVT_PROTOERR = 0x06
# hardware
CMD_IODIR   = 0x03
CMD_IOWRITE = 0x06
CMD_IOREAD  = 0x07
CMD_TXPOWER = 0x0C
# GAP
CMD_ADVDATA = 0x09
CMD_ADVPARA = 0x08
CMD_SETMODE = 0x01
# GAP Discoverable Mode
GAP_NON_DISCOVERABLE = 0x00
GAP_LIMITED_DISCOVERABLE = 0x01
GAP_GENERAL_DISCOVERABLE = 0x02
GAP_BROADCAST = 0x03
GAP_USER_DATA = 0x04
GAP_ENHANCED_BROADCASTING = 0x05
# GAP Connectable Mode
GAP_NON_CONNECTABLE = 0x00
GAP_DIRECTED_CONNECTABLE = 0x01
GAP_UNDIRECTED_CONNECTABLE = 0x02
GAP_SCANNABLE_CONNECTABLE = 0x03
# ADV Parameters
ADV_CHANNELS_ALL = 0x07
ADV_CHANNELS_37_38 = 0x03
ADV_CHANNELS_39 = 0x04
# ADV Data
ADV_ADVDATA   = 0x00
ADV_SRESPDATA = 0x01

