#!/usr/bin/env python3
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

def main(args):
	ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP);
	sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP);
	server = (args[1], int(args[2]));
	client = ("0.0.0.0", 19134);
	sc.setblocking(0);
	ss.setblocking(0);
	sc.bind(client);
	client_addr = None;

	while True:
		try:
			data, addr = ss.recvfrom(16384);
			sc.sendto(data, client_addr);
		except BlockingIOError:
			pass;
		try:
			data, addr = sc.recvfrom(16384);
			client_addr = addr;
			ss.sendto(data, server);
		except BlockingIOError:
			pass;
	return 0;

if __name__ == '__main__':
	sys.exit(main(sys.argv));
