#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import atexit
import signal
import webbrowser
from os import walk, remove, path, chdir, kill
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from shutil import copy2

descriptions = ["Miecraft Pi Edition. v0.1.1. Default game mode: Creative.", "Minecraft Pocket Edition. v0.6.1. Default game mode: Survival."];
binaries = ["minecraft-pi", "minecraft-pe"];

def on_select_versions(event):
	global current_selection;
	description_text["text"] = descriptions[int(event.widget.curselection()[0])];
	current_selection = int(event.widget.curselection()[0]);
	return 0;

def launch():
	subprocess.Popen([binaries[current_selection]]);
	return 0;

def save_settings():
	username = username_entry.get();
	i = 0;

	while len(username) < 7:
		username = username + "\x00";

	mcpi_file = open("/opt/minecraft-pi/minecraft-pi", "r+");
	mcpi_file.seek(0xfa8ca);
	while i < 7:
		mcpi_file.write(username[i]);
		i += 1;
	i = 0;
	mcpi_file.close();

	mcpe_file = open("/opt/minecraft-pi/minecraft-pe", "r+");
	mcpe_file.seek(0xfa8ca);
	while i < 7:
		mcpe_file.write(username[i]);
		i += 1;
	mcpe_file.close();
	return 0;

def on_select_mods(event):
	if mods.get(int(event.widget.curselection()[0])) is not None:
		delete_button["state"] = NORMAL;
	else:
		delete_button["state"] = DISABLED;
	return 0;

def install_mod():
	mod_file = askopenfilename(filetypes=[("Python scripts", "*.py")]);
	copy2(mod_file, "./mods/" + path.basename(mod_file));
	update_mods();
	delete_button["state"] = DISABLED;
	return 0;

def delete_mod():
	remove("./mods/" + mods.get(int(mods.curselection()[0])));
	update_mods();
	delete_button["state"] = DISABLED;
	return 0;

def update_mods():
	mod_files = [];
	i = 0;

	for (_, _, files) in walk("mods"):
		mod_files.extend(files);

	mods.delete(0, END);

	while i < len(mod_files):
		mods.insert(i, mod_files[i]);
		i += 1;
	return 0;

def start_mods():
	global mods_process;
	mods_process = subprocess.Popen(["python3", "mcpim.py"]);
	return 0;

def kill_mods():
	kill(mods_process.pid, signal.SIGTERM);
	return 0;

def change_skin():
	skin_file = askopenfilename(filetypes=[("Portable Network Graphics", "*.png")]);
	copy2(skin_file, "/opt/minecraft-pi/data/images/mob/char.png");
	return 0;

def web_open(event):
	webbrowser.open(event.widget.cget("text"));
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
	versions.insert(0, " Minecraft Pi Edition ");
	versions.insert(1, " Minecraft Pocket Edition ");
	versions.bind('<<ListboxSelect>>', on_select_versions);
	versions.pack(side=LEFT);

	description_text = Label(versions_frame, text="", wraplength=256);
	description_text.pack(pady=48);

	versions_frame.pack(fill=BOTH, expand=True);

	launch_frame = Frame(tab);
	launch_button = Button(launch_frame, text="Launch!", command=launch);
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
	username_text.pack(side=LEFT, anchor=N, pady=16);

	username_entry = Entry(form_frame, width=32);
	username_entry.pack(side=RIGHT, anchor=N, pady=16);
	form_frame.pack();

	buttons_frame = Frame(tab);
	skin_button = Button(buttons_frame, text="Change skin", command=change_skin);
	skin_button.pack(side=LEFT, anchor=S);
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

def about_tab(parent):
	tab = Frame(parent);

	title = Label(tab, text="Minecraft Pi Launcher");
	title.config(font=("", 24));
	title.pack();

	version = Label(tab, text="v0.1.0");
	version.config(font=("", 10));
	version.pack();

	author = Label(tab, text="by @Alvarito050506");
	author.config(font=("", 10));
	author.pack();
	author.bind("<Button-1>", web_open);

	url = Label(tab, text="https://github.com/Alvarito050506/MCPIL", fg="blue", cursor="hand2");
	url.config(font=("", 10));
	url.pack();
	author.bind("<Button-1>", web_open);
	return tab;

def main(args):
	global mods_process;
	chdir(path.dirname(__file__));
	window = Tk();
	window.title("MCPI Laucher");
	window.geometry("480x348");
	window.resizable(False, False);
	window.iconphoto(True, PhotoImage(file="install_files/icon.png"))

	tabs = ttk.Notebook(window);
	tabs.add(play_tab(tabs), text="Play");
	tabs.add(settings_tab(tabs), text="Settings");
	tabs.add(mods_tab(tabs), text="Mods");
	tabs.add(about_tab(tabs), text="About");
	tabs.pack(fill=BOTH, expand=True);

	copy2("/opt/minecraft-pi/data/images/mob/char.png", "/opt/minecraft-pi/data/images/mob/char_original.png");
	start_mods();
	atexit.register(kill_mods);

	window.mainloop();
	return 0;

if __name__ == '__main__':
	sys.exit(main(sys.argv));
