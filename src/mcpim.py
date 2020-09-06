#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  mcpim.py
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
import subprocess
import signal
import atexit
import zlib
import shutil
import time
import glob
from os import kill, remove, path, mkdir, getenv
from mcpi import minecraft

home = getenv("HOME");

def kill_mods():
	i = 0;
	while i < len(mods_processes):
		kill(mods_processes[i].pid, signal.SIGTERM);
		i += 1;
	return 0;

def compile_mods(file_name):
	mod_file = open(file_name, "rb");
	mod_code = zlib.compress(mod_file.read());
	mod_file.close();
	mod_file = open(file_name.replace(".py", ".mcpi"), "wb");
	mod_file.write(mod_code);
	mod_file.close();
	return 0;

def start_mods(args=[]):
	if len(args) > 1:
		compile_mods(args[1]);
		return 0;

	global mods_processes;
	mods_processes = [];
	mod_files = [];
	i = 0;
	j = None;

	try:
		while j is None:
			try:
				minecraft.Minecraft.create();
				mod_files = glob.glob(home + "/.mcpil/mods/*.mcpi");
				while i < len(mod_files):
					mod_file = open(mod_files[i], "rb");
					mod_code = zlib.decompress(mod_file.read()).decode("utf-8");
					mod_file.close();
					mod_name = home + "/.mcpil/mods/." + path.basename(mod_files[i]).replace(".mcpi", ".py");
					mod_file = open(mod_name, "w");
					mod_file.write(mod_code);
					mod_file.close();
					subprocess.Popen(["python3", mod_name]);
					time.sleep(5);
					remove(mod_name);
					i += 1;
				atexit.register(kill_mods);
				j = 1;
			except ConnectionRefusedError:
				pass;
	except KeyboardInterrupt:
		j = 1;
		kill_mods();
		pass;
	return 0;

if __name__ == "__main__":
	sys.exit(start_mods(sys.argv));
