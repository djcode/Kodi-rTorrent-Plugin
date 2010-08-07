#!/usr/bin/python

"""
rtorrent.py
Version 0.1

Created by Brian Partridge on 2008-06-28.
Copyright (c) 2008 Brian Partridge. All rights reserved.
"""

import xmlrpclib
import sys

class RtorrentFault(Exception):
	def __init__(self, msg):
		self.msg = msg

class File(dict):
	"""Represents a file within a transfer."""
	def __init__(self, infohash, index, server):
		dict.__init__(self)
		self['hash'] = infohash
		self['index'] = index
		self.server = server
		self.update()
	
	def update(self):
		"""Retrieve the latest data about a file."""
		m = xmlrpclib.MultiCall(self.server)
		m.f.get_path(self['hash'], self['index'])
		m.f.get_priority(self['hash'], self['index'])

		results = m()

		self['name'] = results[0]
		self['priority'] = results[1]

	def setPriority(self, priority):
		"""Sets the priority of a file.\n0=off, 1=normal, 2=high."""
		self.server.f.set_priority(self['hash'], self['index'], priority)

		
class Transfer(dict):
	"""Represents an individual transfer within rtorrent."""
	def __init__(self, infohash, server):
		dict.__init__(self)
		self['hash'] = infohash
		self.server = server
		self.files = []
		self.update()
	
	def update(self):
		"""Retrieve the latest data about a transfer."""
		m = xmlrpclib.MultiCall(self.server)
		m.d.get_name(self['hash'])
		m.d.get_size_bytes(self['hash'])
		m.d.get_base_path(self['hash'])
		m.d.get_state(self['hash'])
		m.d.get_down_rate(self['hash'])
		m.d.get_up_rate(self['hash'])
		m.d.get_down_total(self['hash'])
		m.d.get_up_total(self['hash'])
		m.d.get_ratio(self['hash'])
		m.d.get_custom1(self['hash'])
		m.d.get_custom2(self['hash'])
		m.d.get_custom3(self['hash'])
		m.d.get_custom4(self['hash'])
		m.d.get_custom5(self['hash'])
		m.d.get_size_files(self['hash'])

		results = m()
		
		self['name'] = results[0]
		self['size'] = results[1]
		self['path'] = results[2]
		self['state'] = results[3]
		self['down_rate'] = results[4]
		self['up_rate'] = results[5]
		self['down_total'] = results[6]
		self['up_total'] = results[7]
		self['ratio'] = results[8]
		self['custom1'] = results[9]
		self['custom2'] = results[10]
		self['custom3'] = results[11]
		self['custom4'] = results[12]
		self['custom5'] = results[13]
		self['num_files'] = results[14]

	def updateFiles(self):
		if self.files:
			for f in self.files:
				f.update()
		else:
			for i in range(self['num_files']):
				self.files.append(File(self['hash'], i, self.server))
		
	def setDirectory(self, directory):
		"""Sets the destination directory for the transfer."""
		self.server.d.set_directory(self['hash'], directory)

	def setCustom(self, num, value):
		"""Sets a custom string on the transfer."""
		methods = {
					1:self.server.d.set_custom1, 
					2:self.server.d.set_custom2, 
					3:self.server.d.set_custom3, 
					4:self.server.d.set_custom4, 
					5:self.server.d.set_custom5
				}
		methods[num](self['hash'], str(value))
		
	def start(self):
		self.server.d.start(self['hash'])
		
	def stop(self):
		self.server.d.stop(self['hash'])

	def close(self):
		self.server.d.close(self['hash'])
		
	def __cmp__(self, rhs):
		"""Used to sort Transfers by name."""
		return cmp(self['name'], rhs['name'])
		
class RtorrentProxy(dict):
	"""Represents an rtorrent client running on the host at 'server_url'.\nAllows query and control operations on a remote rtorrent process."""
	def __init__(self, server_url):
		try:
			self.server = xmlrpclib.ServerProxy(server_url)
		except IOError, e:
			# log the error too
			print "IOError:", e
			raise RtorrentFault("Invalid URL.")
		self.url = server_url
		self.transfers = []
		self.update()

	def update(self):
		"""Retrieves the latest data about the state of rtorrent."""
		#TODO: Get total up, total down, throttle, etc values
		pass

	def updateTransfers(self):
		"""Retrieves the latest data about the state of rtorrent and it's transfers."""
		try:
			hashes = self.server.download_list("main")
		except xmlrpclib.ProtocolError, e:
			# log the error too
			print "%s %d %s" % (e.url, e.errcode, e.errmsg)
			raise RtorrentFault("An error occured while communicating with the server.")
		except xmlrpclib.Fault, e:
			print e.faultCode, e.faultString
			raise RtorrentFault("An XMLRPC error occurred.")

		# Create a new list of Transfers
		transfers = []
		for h in hashes:
			# If the Transfer is already in the list, get updated data
			for t in self.transfers:
				if h == t['hash']:
					t.update()
					transfers.append(t)
			# Otherwise, create a new Transfer
			else:
				transfers.append(Transfer(h, self.server))
		# Replace the old list with the new list
		self.transfers = transfers
		
	def load(self, filename, directory=None, metadata = {}, start=False, raw=False, verbose=False):
		"""Loads torrent and sets up to 5 custom values (strings) on the transfer"""
		# Initialize additional actions to ''
		commands = []

		# If a specific directory is specified, prepare the action
		if directory:
			commands.append('d.set_directory="%s"' % (directory))

		for i in range(1,6):
			if metadata.has_key(i):
				commands.append('d.set_custom%d="%s"' % (i, metadata[i]))

		if raw:
			torrent = xmlrpclib.Binary(open(filename).read())
			if start:
				# There is no load_raw_start_verbose
				method = self.server.load_raw_start 
			else:
				method = self.server.load_raw_verbose if verbose else self.server.load_raw
		else:
			torrent = filename
			if start:
				method = self.server.load_start_verbose if verbose else self.server.load_start
			else:
				method = self.server.load_verbose if verbose else self.server.load

		# Concatenate the additional commands
		finalcommands = ";".join(commands)
		method(torrent, finalcommands)

def DisplayTransfer(transfer, verbose=False):
		print "%s d %d u %d" %(transfer['name'], transfer['down_rate'], transfer['up_rate'])
		if verbose:
			print "1:%s 2:%s 3:%s 4:%s 5:%s" %(transfer['custom1'], transfer['custom2'], transfer['custom3'], transfer['custom4'], transfer['custom5'])
			for f in transfer.files:
				print "  ",f['priority'],"  ",f['name']

def main(argv=None):
	try:
		bVerbose = False
		server_url = "http://localhost"
		server_url = "http://192.168.1.153"
		client = RtorrentProxy(server_url)
		client.updateTransfers()
		client.transfers.sort()
		for t in client.transfers:
		    if bVerbose:
		        t.updateFiles()
			DisplayTransfer(t, bVerbose)

	except RtorrentFault, e:
		print e.msg


if __name__ == "__main__":
	sys.exit(main())
