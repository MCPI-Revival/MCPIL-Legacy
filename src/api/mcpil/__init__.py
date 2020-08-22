#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
#
#  __init__.py
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
import psutil
from os import environ

def get_user_name():
	return environ.get("MCPIL_USERNAME");

def get_world_name():
	mcpi_process = psutil.Process(int(environ.get("MCPIL_PID")));
	return mcpi_process.open_files()[-1].path.split("/")[-2];

def get_game_mode():
	world_name = get_world_name();
	world_file = open("/root/.minecraft/games/com.mojang/minecraftWorlds/" + world_name + "/level.dat", "rb");
	world_file.seek(0x16);
	game_mode = int.from_bytes(world_file.read(1), "little");
	world_file.close();
	return game_mode;
