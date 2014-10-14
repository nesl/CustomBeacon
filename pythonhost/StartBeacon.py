# --- imports ---
from cbeaconpkg.objects import *
from cbeaconpkg.constants import *

# --- create beacon ---
beacon = BLE112()
beacon.autosetup()

# --- 

# -- close beacon serial --
beacon.close()
