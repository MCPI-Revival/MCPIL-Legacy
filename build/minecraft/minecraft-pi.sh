#!/bin/sh

cd $HOME/.mcpil/minecraft || exit

if grep -q okay /proc/device-tree/soc/v3d@7ec00000/status \
	/proc/device-tree/soc/firmwarekms@7e600000/status 2> /dev/null; then
	export LD_PRELOAD=libbcm_host.so.1.0
	export LD_LIBRARY_PATH=./lib/mesa
else
	export LD_LIBRARY_PATH=./lib/brcm
fi

./minecraft-pi
