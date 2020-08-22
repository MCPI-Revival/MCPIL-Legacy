#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
#
#  setup.py
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

from setuptools import setup, find_packages

setup(
	name="mcpil",
	version="v0.1.1",
	description="MCPI API extensions.",
	author="Alvarito050506",
	author_email="donfrutosgomez@gmail.com",
	url="https://github.com/Alvarito050506/MCPIL",
	project_urls={
		"Bug Tracker": "https://github.com/Alvarito050506/MCPIL/issues",
		"Documentation": "https://github.com/Alvarito050506/MCPIL#readme",
		"Source Code": "https://github.com/Alvarito050506/MCPIL",
	},
	packages=["mcpil"],
	install_requires=["psutil>=5.7.0"],
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Environment :: Console",
		"Operating System :: POSIX :: Linux",
		"Programming Language :: Python :: 3 :: Only",
		"License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
	]
);
