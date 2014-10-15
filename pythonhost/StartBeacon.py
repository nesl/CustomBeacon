# --- imports ---
from cbeaconpkg.objects import *
from cbeaconpkg.constants import *

# --- say hello ---
print()
print('-------------------------')
print('      CustomBeacon       ')
print('-------------------------')

# --- create beacon ---
beacon = BLE112()
beacon.autoSetup()

# --- turn on the green LED to indicate setup is done ---
#beacon.setGreenLed(1)
#beacon.setRedLed(0)
	
# --- set transmit power ---
#beacon.setTxPower(TXPOW_HIGH)

# --- set ibeacon data ---
# UUID, major, minor
beacon.setBeaconParams(IBCN_UUID_NESL, IBCN_MAJOR_NESL, 1000)

# --- enable advertisements ---
beacon.enableAdv()

"""
# --- set advertisement rate ---
beacon.setAdvRate(10)




# --- turn on red LED to indicate advertising ---
beacon.setRedLed(1)


# -- close beacon serial --
#beacon.close()
"""
