#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  mcpil.py
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
import atexit
import signal
import webbrowser
import time
import json
import threading
from os import environ, kill, rename, mkdir, uname, getpid, chdir
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from shutil import copy2
from glob import glob
from mcpicentral import APIClient
from mcpip import *
from mcpim import *

descriptions = [
	"Classic Miecraft Pi Edition.\nNo mods.",
	"Modded Miecraft Pi Edition.\nModPi + MCPI-Docker mods without Survival or Touch GUI.",
	"Minecraft Pocket Edition.\nMCPI-Docker mods.",
	"Custom Profile.\nModify its settings in the Profile tab.",
];
preset_features = [
	str(),
	"Fix Bow & Arrow|Fix Attacking|Mob Spawning|Fancy Graphics|Fix Sign Placement|ModPi",
	"Touch GUI|Survival Mode|Fix Bow & Arrow|Fix Attacking|Mob Spawning|Fancy Graphics|Disable Autojump By Default|Fix Sign Placement|Show Block Outlines"
];

features = [
	"Touch GUI",
	"Survival Mode",
	"Fix Bow & Arrow",
	"Fix Attacking",
	"Mob Spawning",
	"Fancy Graphics",
	"Disable Autojump By Default",
	"Fix Sign Placement",
	"Show Block Outlines",
	"ModPi"
];
enabled_features = str();
home = environ["HOME"];
api_client = APIClient(None);
proxy = Proxy();
mod_names = list();
dll_files = list();

class Checkbox(ttk.Checkbutton):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs);
		self.state = BooleanVar(self);
		self.configure(variable=self.state);

	def checked(self):
		return self.state.get();

	def check(self, val):
		return self.state.set(val);

class HyperLink(Label):
	def __init__(self, parent, url, text=None, fg=None, cursor=None, *args, **kwargs):
		self.url = url;
		super().__init__(parent, text=(text or url), fg=(fg or "blue"), cursor=(cursor or "hand2"), *args, **kwargs);
		self.bind("<Button-1>", self.web_open);

	def web_open(self, event):
		return webbrowser.open(self.url);

def basename(path):
	return path.split("/")[-1];

def on_select_versions(event):
	global current_selection;
	try:
		current_selection = event.widget.curselection()[0];
		description_text["text"] = descriptions[current_selection];
	except IndexError:
		pass;
	return 0;

def launch():
	global dummy;

	try:
		environ.update({
			"MCPI_FEATURES": preset_features[current_selection]
		});
	except IndexError:
		environ.update({
			"MCPI_FEATURES": enabled_features[:-1]
		});
	bk = environ.get("LD_PRELOAD") or "";
	if "ModPi" in enabled_features:
		environ.update({
			"LD_PRELOAD": f"/usr/lib/libmodpi.so:{bk}"
		});
	chdir("/opt/minecraft-pi");
	mcpi_process = subprocess.Popen(["/opt/minecraft-pi/minecraft-pi"]);
	environ.update({
		"LD_PRELOAD": bk
	});
	try:
		dummy;
	except:
		dummy = 0;
		start_mods();
	return 0;

def pre_launch():
	launch_thread = threading.Thread(target=launch);
	launch_thread.start();
	return 0;

def save_settings():
	username = username_entry.get();
	i = 0;

	if len(username) < 7:
		username = f"{username}\x00";

	config_file = open(f"{home}/.mcpil/username.txt", "w");
	config_file.seek(0);
	config_file.write(username[:min(len(username), 7)]);
	config_file.close();
	return 0;

def on_select_mods(event):
	try:
		if mods.get(event.widget.curselection()[0]) is not None:
			delete_button["state"] = NORMAL;
		else:
			delete_button["state"] = DISABLED;
	except IndexError:
		pass;
	return 0;

def install_mod(mod_file=None):
	if mod_file is None:
		mod_file = askopenfilename(filetypes=[("Minecraft Pi Mods", "*.mcpi")]);
	copy2(mod_file, f"{home}/.mcpil/mods/{path.basename(mod_file)}");
	update_mods();
	delete_button["state"] = DISABLED;
	return 0;

def delete_mod():
	remove(f"{home}/.mcpil/mods/{mods.get(mods.curselection()[0])}.mcpi");
	update_mods();
	delete_button["state"] = DISABLED;
	return 0;

def update_mods():
	global mod_names;

	i = 0;
	mod_files = list();
	mod_files = glob(f"{home}/.mcpil/mods/*.mcpi");
	mods.delete(0, END);

	for mod in mod_files:
		mod_path = basename(mod.replace(".mcpi", ""));
		mods.insert(i, mod_path);
		mod_names.append(mod_path);
		i += 1;
	return 0;

def update_dlls():
	global dll_files;

	dll_files = list();
	dll_files = glob("/usr/lib/libmcpi-docker/lib*.so");
	bk = environ.get("LD_LIBRARY_PATH") or str();
	environ.update({
		"LD_LIBRARY_PATH": f"/opt/minecraft-pi/minecraft-pi/lib/brcm:/usr/lib/libmcpi-docker:/usr/arm-linux-gnueabihf/lib:{bk}",
		"LD_PRELOAD": ":".join(dll_files)
	});
	return 0;

def update_servers():
	i = 0;
	for server in api_client.servers:
		servers.insert(i, server);
		i += 1;
	return 0;

def on_select_servers(event):
	try:
		if servers.get(event.widget.curselection()[0]) is not None:
			enable_server_button["state"] = NORMAL;
		else:
			enable_serverbutton["state"] = DISABLED;
	except IndexError:
		pass;
	return 0;

def enable_central_server():
	server_name = api_client.servers[servers.curselection()[0]];
	server = api_client.get_server(server_name);
	proxy.stop();
	proxy.set_option("src_addr", server["ip"]);
	proxy.set_option("src_port", int(server["port"]));
	proxy_thread = threading.Thread(target=proxy.run);
	proxy_thread.start();
	return 0;

def save_world():
	old_world_name = old_worldname_entry.get();
	new_world_name = new_worldname_entry.get();
	world_file = open(f"{home}/.minecraft/games/com.mojang/minecraftWorlds/{old_world_name}/level.dat", "rb+");
	new_world = world_file.read().replace(bytes([len(old_world_name), 0x00]).join(bytes(old_world_name.encode())), bytes([len(old_world_name), 0x00]).join(bytes(old_world_name.encode())));
	world_file.seek(0);
	world_file.write(new_world);
	world_file.seek(0x16);
	world_file.write(bytes([game_mode.get()]));
	world_file.close();
	rename(f"{home}/.minecraft/games/com.mojang/minecraftWorlds/{old_world_name}", f"{home}/.minecraft/games/com.mojang/minecraftWorlds/{new_world_name}");
	return 0;

def set_default_worldname(event):
	new_worldname_entry.delete(0, END);
	new_worldname_entry.insert(0, old_worldname_entry.get());
	return True;

def add_server():
	server_addr = server_addr_entry.get();
	server_port = server_port_entry.get();
	proxy.stop();
	proxy.set_option("src_addr", server_addr);
	proxy.set_option("src_port", int(server_port));
	proxy_thread = threading.Thread(target=proxy.run);
	proxy_thread.start();
	return 0;

def save_profile():
	global enabled_features;

	i = 0;
	profile_file = open(f"{home}/.mcpil/profile.txt", "w");
	enabled_features = str();
	for setting in profile_settings:
		checked = int(setting.checked());
		if checked:
			enabled_features += f"{features[i]}|";
		profile_file.write(str(checked));
		i += 1;
	profile_file.close();
	return 0;

def restore_profile():
	global enabled_features;

	i = 0;
	try:
		profile_file = open(f"{home}/.mcpil/profile.txt", "r");
	except FileNotFoundError:
		return -1;
	profile = profile_file.read(7);
	enabled_features = str();
	for setting in profile:
		checked = bool(int(setting));
		profile_settings[i].check(checked);
		if checked:
			enabled_features += f"{features[i]}|";
		i += 1;
	profile_file.close();
	return 0;

def add_checkboxes(parent):
	global profile_settings;

	i = 0;
	profile_settings = list();
	checkbox_frame = Frame(parent);
	for feature in features:
		tmp = Checkbox(checkbox_frame, text=feature);
		tmp.pack(fill=BOTH, anchor=N, padx=8);
		profile_settings.append(tmp);
		i += 1;
	checkbox_frame.pack(fill=X);
	return 0;

def init():
	try:
		mkdir(f"{home}/.mcpil/");
	except FileExistsError:
		pass;

	try:
		mkdir(f"{home}/.mcpil/mods");
	except FileExistsError:
		pass;

	api_client.servers = list();
	update_dlls();
	try:
		api_client.servers = api_client.get_servers()["servers"];
		update_servers();
	except:
		pass;
	return 0;

def bye():
	proxy.stop();
	window.destroy();
	kill(getpid(), signal.SIGTERM);
	return 0;

def play_tab(parent):
	global description_text;

	tab = Frame(parent);

	title = Label(tab, text="Minecraft Pi Launcher");
	title.config(font=("", 24));
	title.pack();

	choose_text = Label(tab, text="Choose a Minecraft version to launch.");
	choose_text.pack(pady=16);

	versions_frame = Frame(tab);
	versions = Listbox(versions_frame, selectmode=SINGLE, width=22);
	versions.insert(0, " Classic MCPI ");
	versions.insert(1, " Modded MCPI ");
	versions.insert(2, " Classic MCPE ");
	versions.insert(3, " Custom Profile ");
	versions.bind('<<ListboxSelect>>', on_select_versions);
	versions.pack(side=LEFT);

	description_text = Label(versions_frame, text="", wraplength=256);
	description_text.pack(pady=48);

	versions_frame.pack(fill=BOTH, expand=True);

	launch_frame = Frame(tab);
	launch_button = Button(launch_frame, text="Launch!", command=pre_launch);
	launch_button.pack(side=RIGHT, anchor=S);
	launch_frame.pack(fill=BOTH, expand=True);
	return tab;

def settings_tab(parent):
	global username_entry;
	tab = Frame(parent);

	title = Label(tab, text="Settings");
	title.config(font=("", 24));
	title.pack();

	form_frame = Frame(tab);
	username_text = Label(form_frame, text="Username (7 characters max):");
	username_text.pack(side=LEFT, anchor=N, pady=16, padx=8);

	username_entry = Entry(form_frame, width=32);
	username_entry.pack(side=RIGHT, anchor=N, pady=16, padx=8);
	form_frame.pack(fill=X);

	buttons_frame = Frame(tab);
	save_button = Button(buttons_frame, text="Save", command=save_settings);
	save_button.pack(side=RIGHT, anchor=S);
	buttons_frame.pack(fill=BOTH, expand=True);
	return tab;

def mods_tab(parent):
	global delete_button;
	global mods;
	tab = Frame(parent);

	title = Label(tab, text="Mods");
	title.config(font=("", 24));
	title.pack();

	mods_frame = Frame(tab);
	mods = Listbox(mods_frame, selectmode=SINGLE, width=22);
	update_mods();
	mods.bind('<<ListboxSelect>>', on_select_mods);
	mods.pack(pady=16);
	mods_frame.pack();

	buttons_frame = Frame(tab);
	start_button = Button(buttons_frame, text="Start mods", command=start_mods);
	start_button.pack(side=RIGHT, anchor=S);
	install_button = Button(buttons_frame, text="Install", command=install_mod);
	install_button.pack(side=RIGHT, anchor=S);
	delete_button = Button(buttons_frame, text="Delete", command=delete_mod, state=DISABLED);
	delete_button.pack(side=RIGHT, anchor=S);
	buttons_frame.pack(fill=BOTH, expand=True);
	return tab;

def worlds_tab(parent):
	global old_worldname_entry;
	global new_worldname_entry;
	global game_mode;
	tab = Frame(parent);

	title = Label(tab, text="Worlds");
	title.config(font=("", 24));
	title.pack();

	old_worldname_frame = Frame(tab);
	old_worldname_text = Label(old_worldname_frame, text="World Name:");
	old_worldname_text.pack(side=LEFT, anchor=N, pady=16, padx=8);

	old_worldname_entry = Entry(old_worldname_frame, width=32, validate="focus", validatecommand=(tab.register(set_default_worldname), "%P"));
	old_worldname_entry.pack(side=RIGHT, anchor=N, pady=16, padx=8);
	old_worldname_frame.pack(fill=X);

	new_worldname_frame = Frame(tab);
	new_worldname_text = Label(new_worldname_frame, text="New World Name:");
	new_worldname_text.pack(side=LEFT, anchor=N, padx=8);

	new_worldname_entry = Entry(new_worldname_frame, width=32);
	new_worldname_entry.pack(side=RIGHT, anchor=N, padx=8);
	new_worldname_frame.pack(fill=X);

	game_mode_frame = Frame(tab);
	game_mode_text = Label(game_mode_frame, text="Game mode:");
	game_mode_text.pack(side=LEFT, anchor=N, pady=16, padx=8);
	game_mode = IntVar();
	game_mode.set(1);
	survival_mode_button = Radiobutton(game_mode_frame, text="Survival", variable=game_mode, value=0, indicatoron=False, width=12);
	creative_mode_button = Radiobutton(game_mode_frame, text="Creative", variable=game_mode, value=1, indicatoron=False, width=12);
	creative_mode_button.pack(side=RIGHT, pady=16, padx=8);
	survival_mode_button.pack(side=RIGHT, pady=16, padx=8);
	game_mode_frame.pack(fill=X);

	buttons_frame = Frame(tab);
	start_button = Button(buttons_frame, text="Save", command=save_world);
	start_button.pack(side=RIGHT, anchor=S);
	buttons_frame.pack(fill=BOTH, expand=True);
	return tab;

def servers_tab(parent):
	global server_addr_entry;
	global server_port_entry;
	tab = Frame(parent);

	title = Label(tab, text="Servers");
	title.config(font=("", 24));
	title.pack();

	server_addr_frame = Frame(tab);
	server_addr_text = Label(server_addr_frame, text="Server addres:");
	server_addr_text.pack(side=LEFT, anchor=N, pady=16, padx=8);

	server_addr_entry = Entry(server_addr_frame, width=32);
	server_addr_entry.pack(side=RIGHT, anchor=N, pady=16, padx=8);
	server_addr_frame.pack(fill=X);

	server_port_frame = Frame(tab);
	server_port_text = Label(server_port_frame, text="Server port:");
	server_port_text.pack(side=LEFT, anchor=N, padx=8);

	server_port_entry = Entry(server_port_frame, width=32);
	server_port_entry.pack(side=RIGHT, anchor=N, padx=8);
	server_port_frame.pack(fill=X);

	buttons_frame = Frame(tab);
	start_button = Button(buttons_frame, text="Add server", command=add_server);
	start_button.pack(side=RIGHT, anchor=S);
	buttons_frame.pack(fill=BOTH, expand=True);
	return tab;

def central_tab(parent):
	global servers;
	global enable_server_button;
	tab = Frame(parent);

	title = Label(tab, text="MCPI Central");
	title.config(font=("", 24));
	title.pack();

	public = Label(tab, text="Public servers");
	public.config(font=("", 10));
	public.pack();

	servers_frame = Frame(tab);
	servers = Listbox(servers_frame, selectmode=SINGLE, width=22);
	servers.bind('<<ListboxSelect>>', on_select_servers);
	servers.pack(pady=16);
	servers_frame.pack();

	try:
		update_servers();
	except:
		pass;

	buttons_frame = Frame(tab);
	enable_server_button = Button(buttons_frame, text="Enable server", command=enable_central_server, state=DISABLED);
	enable_server_button.pack(side=RIGHT, anchor=S);
	buttons_frame.pack(fill=BOTH, expand=True);
	return tab;

def profile_tab(parent):
	global profile_settings;
	tab = Frame(parent);

	title = Label(tab, text="Custom Profile");
	title.config(font=("", 24));
	title.pack();

	add_checkboxes(tab);
	restore_profile();

	buttons_frame = Frame(tab);
	start_button = Button(buttons_frame, text="Save", command=save_profile);
	start_button.pack(side=RIGHT, anchor=S);
	buttons_frame.pack(fill=BOTH, expand=True);
	return tab;

def about_tab(parent):
	tab = Frame(parent);

	title = Label(tab, text="Minecraft Pi Launcher");
	title.config(font=("", 24));
	title.pack();

	version = Label(tab, text="v0.7.1");
	version.config(font=("", 10));
	version.pack();

	author = HyperLink(tab, "https://github.com/Alvarito050506", text="by @Alvarito050506", fg="black");
	author.config(font=("", 10));
	author.pack();

	url = HyperLink(tab, "https://github.com/MCPI-Devs/MCPIL");
	url.config(font=("", 10));
	url.pack();
	return tab;

def main(args):
	arch = uname()[4];
	if "arm" not in arch and "aarch" not in arch:
		sys.stderr.write("Error: Minecraft Pi Launcher must run on a Raspberry Pi.\n");
		return -1;

	global mods_process;
	global window;

	window = Tk();
	window.title("MCPI Laucher");
	window.geometry("480x348");
	window.resizable(False, False);
	window.iconphoto(True, PhotoImage(file="/usr/share/icons/hicolor/48x48/apps/mcpil.png"));

	init_thread = threading.Thread(target=init);
	init_thread.start();

	tabs = ttk.Notebook(window);
	tabs.add(play_tab(tabs), text="Play");
	tabs.add(settings_tab(tabs), text="Settings");
	tabs.add(mods_tab(tabs), text="Mods");
	tabs.add(worlds_tab(tabs), text="Worlds");
	tabs.add(servers_tab(tabs), text="Servers");
	tabs.add(central_tab(tabs), text="Central");
	tabs.add(profile_tab(tabs), text="Profile");
	tabs.add(about_tab(tabs), text="About");
	tabs.pack(fill=BOTH, expand=True);

	if len(args) > 1:
		install_mod(args[1]);

	window.wm_protocol("WM_DELETE_WINDOW", bye);

	try:
		window.mainloop();
	except KeyboardInterrupt:
		bye();
	return 0;

if __name__ == "__main__":
	sys.exit(main(sys.argv));
