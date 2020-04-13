#!/usr/bin/env python3
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
import os
import shutil
import fileinput

def main():
	if "arm" not in os.uname()[4] and "aarch" not in os.uname()[4]:
		sys.stdout.write("Error: Minecraft Pi Launcher must run on a Raspberry Pi.\n");
		return 1;

	if os.geteuid() != 0:
		sys.stdout.write("Error: You need to have root privileges to run this installer.\n");
		return 1;

	sys.stdout.write("Installing dependencies... ");
	subprocess.call(["sudo", "apt-get", "install", "python3-tk", "wget", "bspatch", "-qq"]);
	subprocess.call(["sudo", "pip3", "install", "psutil", "-qq"]);
	sys.stdout.write("OK.\n");

	sys.stdout.write("Downloading Minecraft... ");
	subprocess.call(["sudo", "apt-get", "install", "minecraft-pi", "-qq"]);
	sys.stdout.write("OK.\n");

	sys.stdout.write("Installing Minecraft... ");
	subprocess.call(["bspatch", "/opt/minecraft-pi/minecraft-pi", "/opt/minecraft-pi/minecraft-pe", "./.install_files/minecraft-pe.bsdiff"]);
	subprocess.call(["chmod", "a+x", "/opt/minecraft-pi/minecraft-pe"]);
	sys.stdout.write("OK.\n");

	sys.stdout.write("Installing API... ");
	subprocess.call(["python3", "./api/setup.py", "-q", "install"]);
	sys.stdout.write("OK.\n");

	sys.stdout.write("Configuring... ");
	
	desktop_template = open("./.install_files/tk.mcpi.mcpil.desktop", "r");
	desktop_file = open("/usr/share/applications/tk.mcpi.mcpil.desktop", "w");
	desktop_file.write(desktop_template.read().replace("$(EXECUTABLE_PATH)", os.getcwd() + "/mcpil.py").replace("$(ICON_PATH)", os.getcwd() + "/.install_files/icon.png"));
	desktop_template.close();
	desktop_file.close();

	shutil.copy2("./.install_files/minecraft-pe", "/usr/bin/minecraft-pe");
	subprocess.call(["chmod", "a+x", "/usr/bin/minecraft-pe"]);
	subprocess.call(["chmod", "a+x", "mcpil.py"]);

	shutil.copy2("./.install_files/icon.png", "/usr/share/pixmaps/mcpil.png");
	shutil.copy2("./.install_files/application-x-mcpimod.png", "/usr/share/pixmaps/application-x-mcpimod.png");
	shutil.copy2("./.install_files/mcpimod.xml", "/usr/share/mime/packages/application-x-mcpimod.xml");
	subprocess.call(["update-mime-database", "/usr/share/mime"]);
	sys.stdout.write("OK.\n");
	return 0;

if __name__ == '__main__':
	sys.exit(main());
