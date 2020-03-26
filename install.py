#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

	sys.stdout.write("Installing dependencies... ");
	subprocess.call(["sudo", "apt-get", "install", "python3-tk", "wget", "bspatch", "-qq"]);
	sys.stdout.write("OK.\n");

	sys.stdout.write("Downloading Minecraft... ");
	subprocess.call(["sudo", "apt-get", "install", "minecraft-pi", "-qq"]);
	sys.stdout.write("OK.\n");

	sys.stdout.write("Installing Minecraft... ");
	subprocess.call(["bspatch", "/opt/minecraft-pi/minecraft-pi", "/opt/minecraft-pi/minecraft-pe", "install_files/minecraft-pe.bsdiff"]);
	subprocess.call(["chmod", "a+x", "/opt/minecraft-pi/minecraft-pe"]);
	sys.stdout.write("OK.\n");

	sys.stdout.write("Configuring... ");
	
	desktop_template = open("install_files/mcpil.desktop", "r");
	desktop_file = open("/usr/share/applications/mcpil.desktop", "w");
	desktop_file.write(desktop_template.read().replace("$(EXECUTABLE_PATH)", os.getcwd() + "/mcpil.py").replace("$(ICON_PATH)", os.getcwd() + "/install_files/icon.png"));
	desktop_template.close();
	desktop_file.close();
	
	shutil.copy2("./install_files/minecraft-pe", "/usr/bin/minecraft-pe");
	subprocess.call(["chmod", "a+x", "/usr/bin/minecraft-pe"]);
	subprocess.call(["chmod", "a+x", "mcpil.py"]);
	sys.stdout.write("OK.\n");
	return 0;

if __name__ == '__main__':
	sys.exit(main());
