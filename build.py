#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
#
#  build.py
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
import py_compile
import glob
from os import chdir

def main(args):
	src = glob.glob("./src/*.py");
	i = 0;
	while i < len(src):
		py_compile.compile(src[i], cfile="./build/" + src[i].replace("./src", "").replace(".py", ".pyc"), optimize=2);
		i += 1;
	
	return 0;

if __name__ == '__main__':
	sys.exit(main(sys.argv));
