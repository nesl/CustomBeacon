# -- BLE112 adapter board hardware --
LED_PORT      = 1
LED_PIN_GREEN = 0
LED_PIN_RED   = 1
CMD_WAIT_DEFAULT = (0.05) # 50 ms

# -- transmit powers
TXPOW_LOW     = 0
TXPOW_AVG     = 7
TXPOW_HIGH    = 15

# -- calibrated 1 meter RX powers
# powers from 0 to 15, -23 to +3 dBm
TXPOW_1M_ARRAY = [0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5]
