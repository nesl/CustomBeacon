# --- imports ---
import re
import sys
import os
from serial import Serial
import threading
import time
import struct
from ..constants import *

class BLE112:
	
	def __init__(self, devpath=''):
		self.devpath = devpath
		self.hw_addr = ''
		self.baud = 115200
		self.serialdev = None
		self.isopen = False
		self.devgood = False
		self.txpower = 0
		
	def setMode(self, disc, connect):
		print('Setting BLE112 Mode...')
		# payload is [GAP discoverable mode, GAP connectable mode]
		self.createAndSendCmdPacket(CID_GAP, CMD_SETMODE, [disc, connect])
		
	def setAdvData(self, data):
		print('Setting Adv data...')
		if len(data) > 31:
			print('    > data is longer than 31 bytes, aborting!')
			return
			
		payload = [ADV_ADVDATA]
		payload.extend(data)
		self.createAndSendCmdPacket(CID_GAP, CMD_ADVDATA, payload)
		
	def constructAdvPacket(self, advTypes, payload):
		# length of advertisement types
		len_types = len(advTypes)
		# length of payload
		len_payload = len(payload)
		# total packet length
		len_total = 2 + len_types + len_payload
		# check to make sure length doesn't exceed 31
		if len_total > 31:
			print('  Error: advertisement packet exceeds 31 bytes')
			return None
		# construct packet
		packet = bytearray([len_total, len_types])
		packet.extend(advTypes)
		packet.extend([len_payload])
		packet.extend(payload)
		#print('adv payload = ' + ''.join('{:02x} '.format(x) for x in packet))
		
		return packet
		
		
	def setAdvRate(self, desired_rate_hz):
		print('Setting BLE112 Adv. Rate...')
		# make sure rate is in good range (20ms to 10s)
		if desired_rate_hz > 20:
			print('    > requested rate too high, setting to 20 Hz')
			desired_rate_hz = 20
		if desired_rate_hz < 0.10:
			print('    > requested rate too low, setting to 0.10 Hz')
			desired_rate_hz = 0.10
	
		# convert desired rate to byte-value (0x20 (20ms) to 0x4000 (10+s) in steps of 625us)
		desired_interval_ms = round((1e3*1.0/desired_rate_hz))
		desired_interval_ticks = round(desired_interval_ms/0.625)
		
		# rate is specified by desired +/- 30ms
		int_ticks_min = desired_interval_ticks-48
		int_ticks_max = desired_interval_ticks+48
		
		# create payload (bytes are little endian!)
		min_bytes = struct.pack('<H', int_ticks_min)
		max_bytes = struct.pack('<H', int_ticks_max) 
		
		payload = bytearray()
		payload.extend(min_bytes)
		payload.extend(max_bytes)
		payload.extend([ADV_CHANNELS_ALL])
		
		# payload is: [adv_interval_min, adv_interval_max, adv_channels]
		self.createAndSendCmdPacket(CID_GAP, CMD_ADVPARA, payload)
		
	def setTxPower(self, power):
		self.createAndSendCmdPacket(CID_HW, CMD_TXPOWER, [power])	
		self.txpower = power
	
	def setBeaconParams(self, UUID, major, minor):
		# construct adv data array (adv. types, custom adv. payload)
		payload = IBCN_PREFIX
		payload.extend(UUID)
		# make major and minor into 2 byte arrays
		payload.extend(struct.pack('!H', major))
		payload.extend(struct.pack('!H', minor))
		# determine calibrated transmit power
		payload.extend([ TXPOW_1M_ARRAY[self.txpower] ])
		
		advpkt = self.constructAdvPacket(IBCN_TYPES, payload)
		self.setAdvData(advpkt)

	def enableAdv(self):
		self.setMode(GAP_USER_DATA, GAP_NON_CONNECTABLE)
		
	def disableAdv(self):
		self.setMode(GAP_NON_DISCOVERABLE, GAP_NON_CONNECTABLE)

	def autoSetup(self):
		print('Auto-detecting BLE112 (Linux)...')
		devlist = os.listdir('/dev')
		ble_regex = '.*ttyUSB.*'
		candidates = []
		for dev in devlist:
			check = re.match(ble_regex, dev)
			if check is not None:
				candidates.append(dev)

		if len(candidates) is 0:
			print('    > no devices found')
			return

		print('    > found ' + str(len(candidates)) + ' device(s)')
		self.devpath = '/dev/' + candidates[0]
		print('    > opening device: ' + self.devpath)
		# open device
		try:
			self.serialdev = Serial(self.devpath, baudrate=self.baud, timeout=30e-3)
			self.isopen = True
		except Error:
			print('   > Error: unable to open device')
			return
		
		# fire up device listener thread
		self.listener = threading.Thread(target=self.listen)
		self.listener.start()
		
		# check to make sure the BLE device is functioning ok
		print('    > checking BLE health')
		self.probeDevHealth()
		if self.devgood is False:
			print('   > BLE Device has not issued "OK" signal, aborting.')
			return 1
		print('       BLE device is "OK"')
		
		print('    > determining device MAC')
		
		# probe device mac
		self.probeDevAddr()
		print('       Device MAC: ' + ''.join('{:02x} '.format(x) for x in self.hw_addr))
		
		# set starting TX Power
		self.setTxPower(TXPOW_HIGH)
		print('    > setting starting TX Power to HIGH...')
		
		# configure the LED pins
		self.configureLeds()

	def close(self):
		self.serialdev.close()
		
	def configureLeds(self):
		# set IO direction to output (port 1, pins 0 and 1)
		self.createAndSendCmdPacket(CID_HW, CMD_IODIR, [LED_PORT, (1<<LED_PIN_GREEN)+(1<<LED_PIN_RED)])

	def setGreenLed(self, val):
		self.createAndSendCmdPacket(CID_HW, CMD_IOWRITE, [LED_PORT, (1<<LED_PIN_GREEN), (val<<LED_PIN_GREEN)])

	def setRedLed(self, val):
		self.createAndSendCmdPacket(CID_HW, CMD_IOWRITE, [LED_PORT, (1<<LED_PIN_RED), (val<<LED_PIN_RED)])
		
	def probeDevHealth(self):
		pkt = self.createAndSendCmdPacket(CID_SYSTEM, CMD_HELLO, None)

	def probeDevAddr(self):
		self.createAndSendCmdPacket(CID_SYSTEM, CMD_GETADDR, None)

	def createCmdPacket(self, classID, cmdID, payload):
		# message type (0 = cmd/resp)
		MT = 0
		# technology Type (0 = BTSmart)
		TT = 0
		# Payload length
		if payload is None:
			PLL = 0
		else:
			PLL = len(payload)
		# PLL High (3 bits)
		LH = (PLL>>8)&0xFF
		# PLL Low (8 bits)
		LL = PLL&0xFF
		# Class ID
		CID = classID
		# Command ID
		CMD = cmdID
		# Payload
		PL = payload

		# -- create header array
		header = [(MT<<7)+(TT<<3)+(LH), LL, CID, CMD]
		# -- packet array
		if PL is not None:
			header.extend(PL)
		packet = bytes(header)
		
		return packet

	def unpackPacket(self, packet):
		# message type
		MT = (packet[0]>>7)&0x01
		# Command class ID
		CID = packet[2]
		# Command ID
		CMD = packet[3]
		# Payload
		if len(packet) > 4:
			PL = packet[4:]
		else:
			PL = None
		return [MT, CID, CMD, PL]

	def sendPacket(self, packet):
		if self.isopen is not True:
			return
		self.serialdev.write(packet)
		
	def createAndSendCmdPacket(self, classID, cmdID, payload):
		pkt = self.createCmdPacket(classID, cmdID, payload)
		self.sendPacket(pkt)
		print('          >> SENDING: ' + ''.join('{:02x} '.format(x) for x in pkt))
		time.sleep(CMD_WAIT_DEFAULT)
		
	def handleIncomingPacket(self, raw):
		[MT, CID, CMD, PL] = self.unpackPacket(raw)
		PL_str = 'None'
		if PL is not None:
			PL_str = ''.join('{:02x} '.format(x) for x in PL)
		print('          << RECEIVED: MT = %d, CID = %d, CMD = %d, PL = %s' % (MT, CID, CMD, PL_str))
			
		
		# handle address probe responses
		if CID is CID_SYSTEM and CMD is CMD_GETADDR:
			self.hw_addr = PL
			return
			
		# handle health probe responses
		if CID is CID_SYSTEM and CMD is CMD_HELLO:
			self.devgood = True
			return
			
		# handle parsing errors
		if MT is TYPE_EVENT and CID is CID_SYSTEM and CMD is EVT_PROTOERR:
			print('     ! BLE issued protocol error!')
			
		# unhandled packets get here
		#print(' (ignoring incoming packet from BLE)')
			

	# to be threaded
	def listen(self):
		while True:
			# is there any serial data waiting?
			if self.serialdev.inWaiting() > 0:
				rawbytes = self.serialdev.read(1024)
				# check length to ensure packet is not malformed
				if len(rawbytes) < 4:
					self.serialdev.flush()
					continue
				PL_len_high = rawbytes[0]&0x07
				PL_len_low = rawbytes[1]
				PL_len = int(PL_len_high<<7) + int(PL_len_low)
				if len(rawbytes) is not 4 + PL_len:
					self.serialdev.flush()
					continue
				# hand off the packet
				self.handleIncomingPacket(rawbytes)
				
			






























		






















