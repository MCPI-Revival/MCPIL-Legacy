#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
#
#  mcpip.py
#  
#  Copyright 2020 Alvarito050506 <donfrutosgomez@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 2 of the License.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
import socket
import struct

def decode_packet(data):
	if data[4] == 0x00:
		packet = {
			"iteration": data[1],
			"encapsulation": data[4],
			"length": int(struct.unpack("!H", data[5:7])[0] / 8),
			"id": data[7],
			"data": data[8:-1] + bytes([data[-1]])
		};
	elif data[4] == 0x40:
		packet = {
			"iteration": data[1],
			"encapsulation": data[4],
			"length": int(struct.unpack("!H", data[5:7])[0] / 8),
			"id": data[10],
			"data": data[11:-1] + bytes([data[-1]])
		};
	elif data[4] == 0x60:
		packet = {
			"iteration": data[1],
			"encapsulation": data[4],
			"length": int(struct.unpack("!H", data[5:7])[0] / 8),
			"id": data[14],
			"data": data[15:-1] + bytes([data[-1]])
		};
	else:
		print(data);
	return packet;

class Proxy:
	def __init__(self):
		self.start = False;
		self.__options = {
			"src_addr": None,
			"src_port": 19132,
			"dst_port": 19133
		};

	def set_option(self, name, value):
		if name in self.__options:
			self.__options[name] = value;
		else:
			raise NameError(name);
		return self.__options;

	def get_options(self):
		return self.__options;

	def run(self):
		dst_addr = ("0.0.0.0", self.__options["dst_port"]);
		src_addr = (self.__options["src_addr"], self.__options["src_port"]);
		client_addr = None;
		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP);
		self.__socket.bind(dst_addr);

		while True:
			data, addr = self.__socket.recvfrom(4096);
			if addr == src_addr:
				self.__socket.sendto(data, client_addr);
				if self.start == True:
					print("[S --> C]: ".encode("utf-8") + data);
			else:
				if client_addr is None or client_addr[0] == addr[0]:
					client_addr = addr;
					#if data[0] == 0x84 and data[7] == 0x89:
					#	print(data);
					if data[0] == 0x84:
						if decode_packet(data)["id"] == 0x00 and decode_packet(data)["encapsulation"] == 0x40 and decode_packet(data)["length"] == 0x09:
							self.start = True;
					if self.start == True:
						print("[C --> S]: ".encode("utf-8") + data);
					self.__socket.sendto(data, src_addr);
		return 0;

if __name__ == '__main__':
	args = sys.argv;
	if len(args) < 2:
		print("Error: You must provide a source address.");
		print("Usage: " + args[0] + " src_addr [src_port [dst_port]]");
		print("Where src_addr is a valid internet address and src_port and dst_port are valid internet ports.")
		sys.exit(-1);

	proxy = Proxy();
	proxy.set_option("src_addr", args[1]);
	if len(args) > 2:
		proxy.set_option("src_port", int(args[2]));
	if len(args) > 3:
		proxy.set_option("dst_port", int(args[3]));
	options = proxy.get_options();
	print(options["src_addr"] + ":" + str(options["src_port"]) + " --> 0.0.0.0:" + str(options["dst_port"]));
	try:
		proxy.run();
	except KeyboardInterrupt:
		print("");
		sys.exit(0);
