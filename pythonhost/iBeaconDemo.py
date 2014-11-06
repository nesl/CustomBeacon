# --- imports ---
import time
from cbeaconpkg.objects import *
from cbeaconpkg.constants import *

# --- say hello ---
print()
print('-------------------------')
print('      CustomBeacon       ')
print('-------------------------')

# --- create beacon ---
ble = BLE112()
res = ble.autoSetup()

if res == SUCCESS:

	# --- turn on the green LED to indicate setup is done ---
	ble.setGreenLed(1)
	ble.setRedLed(0)
		
	# --- set transmit power ---
	ble.setTxPower(TXPOW_LOW)

	# --- set ibeacon data ---
	# UUID, major, minor
	ble.setBeaconParams(IBCN_UUID_NESL, IBCN_MAJOR_NESL, 2000)

	# --- set advertisement rate ---
	# below gives error 0x0212 - invalid param?
	ble.setAdvRate(10)

	# --- enable advertisements ---
	ble.enableAdv()

	# --- turn on red LED to indicate advertising ---
	ble.setRedLed(1)
	ble.setGreenLed(0)

	# -- close beacon serial --
	#ble.close()

