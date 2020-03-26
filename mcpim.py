#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import signal
import atexit
from os import walk, kill
from mcpi import *

def kill_mods():
	i = 0;
	while i < len(mods_processes):
		kill(mods_processes[i].pid, signal.SIGTERM);
		i += 1;
	return 0;

def main():
	global mods_processes;
	mods_processes = [];
	mod_files = [];
	i = 0;
	j = None;

	while j is None:
		try:
			minecraft.Minecraft.create();
			for (_, _, files) in walk("mods"):
				mod_files.extend(files);
			while i < len(mod_files):
				subprocess.Popen(["python3", "mods/" + mod_files[i]]);
				i += 1;
			atexit.register(kill_mods);
			j = 1;
		except:
			pass;
	return 0;

if __name__ == '__main__':
	sys.exit(main());
