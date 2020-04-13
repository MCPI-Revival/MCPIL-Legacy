# MCPIL
Minecraft Pi Launcher

![screenshot](https://raw.githubusercontent.com/Alvarito050506/MCPIL/master/screenshot.png)

A simple launcher for Minecraft: Pi Edition.

## Getting started
### Prerequisites
To use MCPIL you need to have `Python >= 3.7.x` pre-installed and root privileges.

### Installation
To install MCPIL, download or clone the repository:
```shell
git clone https://github.com/Alvarito050506/MCPIL.git
```
and then run the `install.py` file. It will create a desktop file that you can access in the "Games" category.

## Features
+ Switch between Minecraft Pi and PE
+ Username change
+ Skin change
+ Mod load
+ Mod API
+ Mod compilation
+ World game mode and name change
+ Join non-local servers
+ Coming soon: Pi Realms

## Usage
Launch the MCPIL desktop file or run the `mcpil.py` file to see the magick! :wink:

## API
There is an MCPIL API that you can use by importing the `mcpil` module into your Python mod. It exposes the following functions:

### `def get_user_name()`
Returns the user name of the player.

### `def get_world_name()`
Returns the name of the current world.

### `def get_game_mode()`
Returns the game mode of the current world as an interger:
 + 0 = Survival
 + 1 = Creative

## Mod compilation
To compile (compress) a Python mod, run the `mcpim.py` file passing the filename of the mod as the first argument. For example:
```shell
./mcpim.py example.py
```
will produce a `example.mcpi` mod file.

## Thanks
To [@Phirel](https://www.minecraftforum.net/members/Phirel) for his Pi2PE (a.k.a. "survival") patch.

## Licensing
All the code of this project is licensed under the [GNU General Public License version 2.0](https://github.com/Alvarito050506/MCPIL/blob/master/LICENSE) (GPL-2.0).

All the documentation of this project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0) license.

![CC BY-SA 4.0](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)
