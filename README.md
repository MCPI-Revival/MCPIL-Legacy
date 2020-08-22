# MCPIL
Minecraft Pi Launcher

![screenshot](https://raw.githubusercontent.com/Alvarito050506/MCPIL/master/screenshot.png)

A simple launcher for Minecraft: Pi Edition.

## Getting started
### Prerequisites
To use MCPIL you need to have Python 3.7 pre-installed.

### Installation
To install MCPIL, download or clone the repository and run the `build.py` file in the root of the repo:
```shell
git clone https://github.com/MCPI-Devs/MCPIL.git
cd ./MCPIL/
python3.7 ./build.py
```
It will generate a `install.pyc` file under the `build` directory, run it:
```shell
cd ./build/
python3.7 ./install.pyc
```
It will "install" MCPI and MCPE, and configure the Launcher.

## Features
+ Switch between Minecraft Pi and PE
+ Username changing
+ Skin changing
+ Mod loading
+ Mod API
+ Mod compilation
+ World setting (game mode and name) changing
+ Join non-local servers
+ Coming soon: More stuff

## Usage
Launch the MCPIL desktop file or run the `mcpil.pyc` file in the `build` folder as following to see the magic! :wink:
```shell
python3.7 ./mcpil.pyc
```

## API
**Warning**: The API will be refactored in the next release.

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
python3.7 ./mcpim.pyc example.py
```
This will produce an `example.mcpi` mod file.

## Thanks
To [@Phirel](https://www.minecraftforum.net/members/Phirel) for his Pi2PE (a.k.a. "survival") patch.

## Licensing
All the code of this project is licensed under the [GNU General Public License version 2.0](https://github.com/Alvarito050506/MCPIL/blob/master/LICENSE) (GPL-2.0).

All the documentation of this project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0) license.

![CC BY-SA 4.0](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)
