# Qtile Configuration

This repository holds configuration for the [Qtile](https://qtile.org) tiling
window manager.

* `.local/qtile` : Setup for running Qtile within a virtual environment.
* `.config/qtile` : Qtile configuration.
* `.config/picom` : picom X11 compositor config
* `.config/powerline` : Shell powerline config.

Clone: `git clone https://github.com/cweave72/qtile`

Tested with:
* Python 3.11
* Ubuntu 25.04

## Setting up to run Qtile from virtual environment

Requirement: `uv` installed.

1. Install linux dependencies:
  * xserver-xorg-core
  * xserver-xorg-input-libinput
  * xinit

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

Example for specifying a single screen: .env:
```
NUM_SCREENS=1
```

## picom

The picom X11 compositor allows effects such as corner radius and blurring.

Install picom:
```
sudo apt install picom
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

