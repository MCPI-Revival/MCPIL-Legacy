<h1 align="center">MCPIL</h1>
<p align="center">
	A simple launcher for Minecraft: Pi Edition.
</p>
<p align="center">
	<a href="https://github.com/MCPI-Devs/MCPIL/blob/master/LICENSE">
		<img src="https://img.shields.io/github/license/MCPI-Devs/MCPIL?label=License" alt="GPL-2.0"></img>
	</a>
	<a href="https://bestpractices.coreinfrastructure.org/projects/4335">
		<img src="https://bestpractices.coreinfrastructure.org/projects/4335/badge" alt=CII Best Practices"></img>
	</a>																								   
	<a href="https://python.org">
		<img src="https://img.shields.io/badge/Python-%E2%89%A53.7.x-blue" alt="Required Python version"></img>
	</a>
	<a href="https://github.com/MCPI-Devs/MCPIL/actions?query=workflow%3ACodeQL">
		<img src="https://github.com/MCPI-Devs/MCPIL/workflows/CodeQL/badge.svg" alt="CodeQL results"></img>
	</a>
</p>
<p align="center">
	<img src="https://raw.githubusercontent.com/Alvarito050506/MCPIL/master/screenshot.png" alt="screenshot"></img>
</p>

### :warning: Warning

This project is broken and very unstable. A lot of bugs are produced by the lack of a good internal design, and breaks the Launcher. See [MCPIL-R](https://github.com/MCPI-Revival/MCPIL) for a version made from the ground up to be way for stable.

If you still want to run this for some reason, an old version of this Launcher like ([v0.6.2](https://github.com/MCPI-Devs/MCPIL/releases/tag/v0.6.2) would be a good choice.

This means the project will **not** be maintained anymore, so PRs or issues won't be fixed/accepted. tl;dr: DO NOT USE THIS!!! USE MCPIL-R!!!

## Getting started
### Prerequisites
To use MCPIL you must have `Python >= 3.7.x` installed on your device prior to using MCPIL.

### Installation
Download and install MCPIL from the releases section:
```shell
wget https://github.com/MCPI-Revival/MCPIL-Legacy/releases/download/v0.7.3/mcpil_0.7.3-1.deb
sudo apt install ./mcpil_0.7.3-1.deb
sudo rm mcpil_0.7.3-1.deb
```

## Features
 + Switch between Minecraft Pi and Minecraft Pocket Edition
 + Username changing
 + Skin changing
 + Mod loading
 + Mod API
 + Mod compilation
 + World settings (gamemode and name) changing
 + Join non-local servers
 + Coming soon: More stuff 

## Usage
Launch the MCPIL desktop file or run the `mcpil` command folder as following to see the magic! :wink:
```shell
mcpil # Yes, simple as this
```

## API
The API documentation was moved to the [ModPi repo](https://github.com/MCPI-Devs/modpi).

The support for the old API was **dropped** in the **v0.5.0 release**! It is recommended to use the new ModPi API. However, the old API documentation is still avaiable [here](https://github.com/MCPI-Devs/MCPIL/tree/3470fb73b81510f5e819a34c04cca6f86457c2b2#api).

## Mod compilation
To compile (compress) a Python mod, run the `mcpim` command passing the filename of the mod as the first argument. For example:
```shell
mcpim ./example.py
```
This will produce an `example.mcpi` mod file.

## Troubleshooting
If you get the `module not found: _tkinter` error, or something of the sort, you can use Homebrew to install a custom tap made by @gamer4life1.
```shell
# First, install brew (If you don't have it already, also make sure to install in /home/linuxbrew/.linuxbrew)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
# Then, apply the custom tap
brew tap gamer4life1/mcpi-tap
# Install gcc (a needed dependency)
brew install gcc
# Follow caveats for gcc (something like example)
export LDFLAGS="-L/home/linuxbrew/.linuxbrew/opt/isl@0.18/lib"
export CPPFLAGS="-I/home/linuxbrew/.linuxbrew/opt/isl@0.18/include"
# Install the custom formula of python (Ignore errors if they say that the system cannot find the bottle, it will compile from source)
brew install custompython
# Finally, add it to your PATH so it is first in your PATH
export PATH="/usr/local/opt/custompython/bin:$PATH"
# Add above to bashrc to load automatically
```

See also [issues](https://github.com/MCPI-Devs/MCPIL/issues) and [discussions](https://github.com/MCPI-Devs/MCPIL/discussions) for future information regarding bugs and errors.

## Thanks
To [@Phirel](https://www.minecraftforum.net/members/Phirel) for his Pi2PE (a.k.a. "survival") patch, and to [@TheBrokenRail](https://thebrokenrail.com) for MCPI-Docker. These two projects were/are highly used & abused by MCPIL :wink:.

To everyone who has or had interest on the project, including MCPI Revival members.

## Licensing
All the code of this project is licensed under the [GNU General Public License version 2.0](https://github.com/Alvarito050506/MCPIL/blob/master/LICENSE) (GPL-2.0).

All the documentation of this project is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0) license.

![CC BY-SA 4.0](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)
