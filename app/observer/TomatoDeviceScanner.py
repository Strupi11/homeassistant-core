import logging
import csv

import requests

class TomatoDeviceScanner:
	# self.logger

	def __init__(self, config):
		self.config = config
		self.logger = logging.getLogger("TomatoDeviceScanner")

		# Read known devices
		with open('tomato_known_devices.csv') as inp:
			known_devices = { row['mac']: row for row in csv.DictReader(inp) }

		# Update known devices csv file for future use
		with open('tomato_known_devices.csv', 'a') as outp:
			writer = csv.writer(outp)

			# Query for new devices
			exec(self.tomato_request("devlist"))

			for name, _, mac, _ in dhcpd_lease:
				if mac not in known_devices:
					writer.writerow((mac, name, 0))

		# Create a dict with ID: NAME of the devices to track
		self.devices_to_track = dict()

		for mac in [mac for mac in known_devices if known_devices[mac]['track'] == '1']:
			self.devices_to_track[mac] = known_devices[mac]['name']
		
		# Doesn't go together with exec: unqualified exec is not allowed in function '__init__' it contains a nested function with free variables
		# self.devices_to_track = {mac: known_devices[mac]['name'] for mac in known_devices if known_devices[mac]['track'] == '1'}


	def get_devices_to_track(self):
		return self.devices_to_track

	def scan_devices(self, triggered_time):
		self.logger.info("Scanning for new devices")
		
		# Query for new devices
		exec(self.tomato_request("devlist"))

		return [mac for iface, mac, rssi, tx, rx, quality, unknown_num in wldev]


	def tomato_request(self, action):
		# Get router info
		r = requests.post('http://{}/update.cgi'.format(self.config.get('tomato','host')), 
							data={'_http_id':self.config.get('tomato','http_id'), 'exec':action}, 
							auth=requests.auth.HTTPBasicAuth(self.config.get('tomato','username'), self.config.get('tomato','password')))

		return r.text	



"""
for ip, mac, iface in arplist:
	pass

# print wlnoise

# print dhcpd_static

for iface, mac, rssi, tx, rx, quality, unknown_num in wldev:
	print mac, quality

print ""

for name, ip, mac, lease in dhcpd_lease:
	if name:
		print name, ip

	else:
		print ip
"""