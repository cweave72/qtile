# Qtile Configuration

This repository holds configuration for the [Qtile](https://qtile.org) tiling
window manager along with other terminal-related tools:

* `.local/qtile` : Setup for running Qtile within a virtual environment.
* `.config/qtile` : Qtile configuration.
* `.config/kitty` : kitty configuration.
* `.config/picom` : picom X11 compositor config
* `.config/powerline` : Shell powerline config.
* `.config/ranger` : A file terminal-based file browser.

Clone: `git clone https://github.com/cweave72/qtile`

Tested with:
* Python 3.11
* Ubuntu 25.04
* Ubuntu 22.04

## Setting up to run Qtile from virtual environment

Requirement: `uv` installed.

1. Install linux dependencies:
  * xserver-xorg-core
  * xserver-xorg-input-libinput
  * xinit
  * libiw-dev

  You can check if you have xorg installed via `dpkg -l | grep xserver-xorg-core`

2. Create symlink in `~/.local`:
```
cd ~/.local
ln -s <path to cloned repo>/qtile/.local/qtile qtile
```

3. Create the virtualenv.
```
cd ~/.local/qtile  (the symlink created in step 2.)
uv sync
```

4. Create the xsession .desktop file: `/usr/share/xsessions/qtile-venv.desktop`:
```
[Desktop Entry]
Name=Qtile (x11)
Comment=Qtile Session within Virtualenv
Exec=/home/cdweave/.local/qtile/qtile-venv-entry.sh
Type=XSession
```
When you reboot, you should see *Qtile (x11)* in your Display Manager options.

## Qtile Config

Create a symlink:
```
cd ~/.config
ln -s <path to cloned repo>/qtile/.config/qtile qtile
```

Within the `~/.config/qtile` directory, create a site-specific `.env` file.
This file is used to set the number of screens being used.

Example for specifying a 2-screen: .env:
```
NUM_SCREENS=2
QTILE_BAR_FONT_SIZE=11
XRANDR_CMD="xrandr --output DP1 --primary --mode 1920x1080 --rate 60.00 --output DP2 --mode 1920x1080 --rate 60.00 --right-of DP1"
```

* `NUM_SCREENS`: The number of screens in the setup (Defaults to 1, max is 2).
* `QTILE_BAR_FONT_SIZE`: Controls the font size in the qtile top and bottom bar.
* `XRANDR_CMD`: A command that is run on startup for setting screen resolution,
  etc...

## picom

The picom X11 compositor allows effects such as corner radius and blurring.

Install picom and dependencies:
```
sudo apt install picom
sudo apt install mesa-utils
```

Create a symlink:
```
cd ~/.config
ln -s <path to cloned repo>/qtile/.config/picom picom
```

## powerline

Adds powerline to the terminal ([docs](www.powerline.readthedocs.io/en/master)).

Since `powerline` is installed in the qtile virtual env, it is helpful to put
symlinks to the powerline exectuables in the `~/.local/bin` directory.

My `~/.local/bin`:
```
drwxrwxr-x 2 cdweave cdweave     4096 Feb 28 14:57 .
drwx------ 6 cdweave cdweave     4096 Feb 21 10:57 ..
lrwxrwxrwx 1 cdweave cdweave       53 Feb 28 11:52 powerline-config -> /home/cdweave/.local/qtile/.venv/bin/powerline-config
lrwxrwxrwx 1 cdweave cdweave       53 Feb 28 14:57 powerline-daemon -> /home/cdweave/.local/qtile/.venv/bin/powerline-daemon
lrwxrwxrwx 1 cdweave cdweave       53 Feb 28 14:46 powerline-render -> /home/cdweave/.local/qtile/.venv/bin/powerline-render
-rwxr-xr-x 1 cdweave cdweave 55484384 Feb 16 06:10 uv
-rwxr-xr-x 1 cdweave cdweave   344368 Feb 16 06:10 uvx
```

Source the `bash_init.sh` script in `.bashrc` to enable powerline.
