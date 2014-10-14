# --- imports ---
import re
import sys
import os
from serial import Serial
import thread
from ..constants import communication

class BLE112:
	
	def __init__(self, devpath=''):
		self.devpath = devpath
		self.mac = ''
		self.baud = 115200
		self.serialdev = None
		self.isopen = False


	def autosetup(self):
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
			self.serialdev = Serial(self.devpath, baudrate=self.baud, timeout=20e-3)
			self.isopen = True
		except Error:
			print('   > Error: unable to open device')
			return
		
		print('    > determining device MAC')
		# find device mac

	def close(self):
		self.serialdev.close()

	def getDevAddr(self):
		# create packet
		pkt = createCmdPacket(CID_SYSTEM, CMD_GETADDR, None)
		# send packet
		self.sendPacket(pkt)
		

	def createCmdPacket(classID, cmdID, payload):
		# message type (0 = cmd/resp)
		MT = 0
		# technology Type (0 = BTSmart)
		TT = 0
		# Payload length
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
		if payload is not None:
			packet = bytes(header.extend(payload))
		else:
			packet = bytes(header)
		
		return packet

	def unpackPacket(packet):
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
		if not self.isopen:
			return
		self.serialdev.write(packet)

	# to be threaded
	def listen(self):

		while True:
			# is there any serial data waiting?
			if self.inWaiting() > 0		
				rawbytes = self.read(1024, timeout=20e-3)
				# check length to ensure packet is not malformed
				if len(rawbytes) < 4:
					continue
				PL_len_high = rawbytes[0]&0x07
				PL_len_low = rawbytes[1]
				PL_len = PL_len_high<<7 + PL_len_low
				if len(rawbytes) is not 4 + PL_len:
					continue
				# parse packet
				
				
			






























		






















