#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
#
#  install.py
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

import subprocess
import sys
from os import uname, getenv, path, makedirs, mkdir, getcwd, chdir
import shutil

def main():
	if "arm" not in uname()[4] and "aarch" not in uname()[4]:
		sys.stdout.write("Error: Minecraft Pi Launcher must run on a Raspberry Pi.\n");
		return 1;

	sizes = ["16", "32", "48", "64", "128"];
	chdir(path.dirname(path.realpath(__file__)));

	if not path.exists(getenv("HOME") + "/.mcpil"):
		subprocess.call(["pip3.7", "install", "--user", "-qq", "psutil"]);
		subprocess.call(["python3.7", "../src/api/setup.py", "-q", "install"]);
		if not path.exists(getenv("HOME") + "/.local/share/applications"):
			makedirs(getenv("HOME") + "/.local/share/applications");
		i = 0;
		while i < len(sizes):
			subprocess.call(["xdg-icon-resource", "install", "--novendor", "--size", sizes[i], "./res/application-x-mcpimod_" + sizes[i] + "px.png", "application-x-mcpimod"]);
			subprocess.call(["xdg-icon-resource", "install", "--novendor", "--size", sizes[i], "./res/mcpil_" + sizes[i] + "px.png", "mcpil"]);
			i += 1;
		subprocess.call(["xdg-mime", "install", "--novendor", "./res/mcpimod.xml"]);
		mkdir(getenv("HOME") + "/.mcpil");
		shutil.copytree("./minecraft", getenv("HOME") + "/.mcpil/minecraft");
		mkdir(getenv("HOME") + "/.mcpil/mods");
		desktop_template = open("./res/tk.mcpi.mcpil.desktop", "r");
		desktop_file = open(getenv("HOME") + "/.local/share/applications/tk.mcpi.mcpil.desktop", "w");
		desktop_file.write(desktop_template.read().replace("$(EXECUTABLE_PATH)", "python3.7 " + getcwd() + "/mcpil.pyc"));
		desktop_template.close();
		desktop_file.close();
	return 0;

if __name__ == '__main__':
	sys.exit(main());
