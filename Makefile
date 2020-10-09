#
#  Makefile
#  
#  Copyright 2020 Alvarito050506 <donfrutosgomez@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; version 3 of the License.
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

pack:
	mkdir -p ./deb/
	mkdir -p ./deb/DEBIAN/
	cp -a ./res/. ./deb/
	mkdir -p ./deb/usr/lib/python3/dist-packages/
	mkdir -p ./deb/usr/bin/
	cp ./src/mcpil.py ./deb/usr/bin/mcpil
	cp ./src/mcpim.py ./deb/usr/lib/python3/dist-packages/
	rm -f ./deb/usr/bin/mcpim
	ln -s /usr/lib/python3/dist-packages/mcpim.py ./deb/usr/bin/mcpim
	sudo chmod a+x ./deb/usr/bin/mcpil
	sudo chmod a+x ./deb/usr/bin/mcpim
	@echo "Package: mcpil" > ./deb/DEBIAN/control
	@echo "Version: 0.7.1" >> ./deb/DEBIAN/control
	@echo "Priority: optional" >> ./deb/DEBIAN/control
	@echo "Architecture: armhf" >> ./deb/DEBIAN/control
	@echo "Depends: libmcpi, mcpi-proxy, mcpi-central, libmodpi, libmcpi-docker, python3, libfreeimage3, libglfw3, minecraft-pi" >> ./deb/DEBIAN/control
	@echo "Maintainer: Alvarito050506 <donfrutosgomez@gmail.com>" >> ./deb/DEBIAN/control
	@echo "Homepage: https://mcpi.tk" >> ./deb/DEBIAN/control
	@echo "Vcs-Browser: https://github.com/MCPI-Devs/MCPIL" >> ./deb/DEBIAN/control
	@echo "Vcs-Git: https://github.com/MCPI-Devs/MCPIL.git" >> ./deb/DEBIAN/control
	@echo "Description: Simple launcher for Minecraft: Pi Edition.\n" >> ./deb/DEBIAN/control
	dpkg-deb -b ./deb/ ./mcpil_0.7.1-1.deb

clean:
	rm -rf ./deb/
	rm -f ./mcpil_*-*.deb
