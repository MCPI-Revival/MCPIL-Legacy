#!/usr/bin/env python3

import sys
import time
from mcpi import *
from mcpil import *

mc = minecraft.Minecraft.create();

def main(args):
	mc.setting("world_immutable", True);
	mc.camera.setFollow();
	mc.saveCheckpoint();
	mc.postToChat("Welcome to Minecraft Pi, " + get_user_name() + ".");
	mc.postToChat("The name of this awesome world is \"" + get_world_name() + "\".");
	if get_game_mode() == 0:
		mc.postToChat("You are in Survival mode.");
	else:
		mc.postToChat("You are in Creative mode.");
	time.sleep(5);
	mc.setting("world_immutable", False);
	mc.setting("nametags_visible", True);
	mc.player.setting("autojump", True);
	mc.camera.setNormal();
	return 0;

if __name__ == '__main__':
	sys.exit(main(sys.argv));
