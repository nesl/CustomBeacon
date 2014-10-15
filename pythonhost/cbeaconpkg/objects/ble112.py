# --- imports ---
import re
import sys
import os
from serial import Serial
import threading
from ..constants.communication import *

class BLE112:
	
	def __init__(self, devpath=''):
		self.devpath = devpath
		self.hw_addr = ''
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
			self.serialdev = Serial(self.devpath, baudrate=self.baud, timeout=30e-3)
			self.isopen = True
		except Error:
			print('   > Error: unable to open device')
			return
		
		# fire up device listener thread
		self.listener = threading.Thread(target=self.listen)
		self.listener.start()
		
		print('    > determining device MAC')
		# probe device mac
		self.probeDevAddr()
		

	def close(self):
		self.serialdev.close()

	def probeDevAddr(self):
		# create packet
		pkt = self.createCmdPacket(CID_SYSTEM, CMD_GETADDR, None)
		# send packet
		self.sendPacket(pkt)
		

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
		if payload is not None:
			packet = bytes(header.extend(payload))
		else:
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
		
	def handleIncomingPacket(self, raw):
		[MT, CID, CMD, PL] = self.unpackPacket(raw)
		
		# handle address probe responses
		if CID is CID_SYSTEM and CMD is CMD_GETADDR:
			self.hw_addr = PL
			print('      Device MAC: ' + ''.join('{:02x} '.format(x) for x in self.hw_addr))

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
				
			






























		






















