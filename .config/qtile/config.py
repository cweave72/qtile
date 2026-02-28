import os
import sys
import re
import os.path as osp
import subprocess
import shlex
import socket
import logging
import logging_tree
from dotenv import load_dotenv

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.lazy import lazy
from libqtile import qtile, layout, bar, hook

from themes import Dracula, Midnight, Monokai, Tomorrow, One_dark, Nordic, Catppuccin

from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

# Note: the system log is in ~/.local/share/qtile/qtile.log
#       the local logger is in ~/.config/qtile/qtile.log
logger = logging.getLogger("myconfig")

#mod = "mod4"   # Windows key
mod = "mod1"   # Alt key

HOME = osp.expanduser('~')
CONFIG_DIR = osp.join(HOME, ".config", "qtile")
ENV_FILE = osp.join(CONFIG_DIR, ".env")


logging.basicConfig(
    filename=osp.join(CONFIG_DIR, "qtile.log"),  
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Load variables from .env file.
logger.info(f"Loading env variables from {ENV_FILE}")
load_dotenv(ENV_FILE)

try:
    NUM_SCREENS = int(os.getenv("NUM_SCREENS"))
except KeyError:
    logger.info(f"Env NUM_SCREENS not set, setting to 1 by default.")
    NUM_SCREENS = 1


def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except socket.error:
            ip = '127.0.0.1'
    return ip


local_ip = get_local_ip()


def bind(key_comb, cmdobj):
    "Helper function for key binding."

    logger.debug('Binding key combination: %s' % key_comb)
    key = [mod]
    m = re.match(r'(\w+)\s*\+?\s*(\w+)?', key_comb)
    if m:
        groups = m.groups(default=None)
        if groups[1] is None:
            char = groups[0]
            logger.debug('binding %s: %r' % (char, cmdobj.__dict__))
        else:
            key.append(groups[0])
            char = groups[1]
            logger.debug('binding mod+%s+%s: %r' % (key[1], char, cmdobj.__dict__))
    else:
        logger.error('No match on regex: %s' % key_comb)
        raise Exception('Bad regex match in bind function')

    return Key(key, char, cmdobj)

term_cmd = "kitty"

# Since we run qtile out of a virtual env, we don't want commands spawned to
# inherit the path to this virtual env. To fix this, we wrap the spawn command
# and modify the env to delete the path to the virtual env prior to launching
# the command.
venv_path = "/home/cdweave/.local/qtile/.venv"
def spawn_no_venv(command):
    env = os.environ.copy()
    #logger.info(f"spawing {command=} {env=}")
    #logger.info(f"VIRTUAL_ENV={env['VIRTUAL_ENV']}")
    #logger.info(f"PATH={env['PATH']}")
    env["PATH"] = env["PATH"].replace(f"{venv_path}/bin:", "")
    env["VIRTUAL_ENV"] = env["VIRTUAL_ENV"].replace(f"{venv_path}", "")
    qtile.spawn(command, env=env)


keys = [
    # Switch between windows in current layout.
    bind("j", lazy.layout.down()),
    bind("k", lazy.layout.up()),
    bind("l", lazy.layout.right()),
    bind("b", lazy.layout.next()),
    bind("n", lazy.layout.normalize()),
    bind("m", lazy.layout.maximize()),
    bind("z", lazy.layout.reset()),
    bind("F11", lazy.layout.grow()),
    bind("F12", lazy.layout.shrink()),

    # Move windows up or down in current stack
    bind("control + j", lazy.layout.shuffle_down()),
    bind("control + k", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    bind("space", lazy.layout.next()),

    # Swap panes of split stack
    bind("shift + space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    bind("shift + Return", lazy.layout.toggle_split()),
    #bind("Return", lazy.spawn("urxvt256c")),
    #bind("Return", lazy.spawn(term_cmd)),
    bind("Return", lazy.function(lambda q: spawn_no_venv(term_cmd))),

    # Toggle between different layouts as defined below
    bind("Tab", lazy.next_layout()),
    bind("q", lazy.window.kill()),

    bind("shift + r", lazy.restart()),
    bind("shift + q", lazy.shutdown()),
    bind("r", lazy.spawn("dmenu_run -p 'dmenu:'")),
]


if NUM_SCREENS == 2:
    keys.append(bind('1', lazy.to_screen(0)))
    keys.append(bind('2', lazy.to_screen(1)))


groups = [Group(i) for i in "asdfghuiop"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        bind(i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        bind("shift + %s" % i.name, lazy.window.togroup(i.name)),
    ])

theme = Nordic
accent_color = None

# Define the layout options
layout_mine = {
    "border_width": 2,
    "border_focus": theme["on"],
    "border_normal": theme["background"],
    "margin": 8,
}

layouts = [
    layout.MonadTall(**layout_mine),
    layout.VerticalTile(**layout_mine),
    layout.MonadWide(**layout_mine),
    layout.Max(**layout_mine),
]

powerline = {
    "decorations": [
        PowerLineDecoration(path='forward_slash')
    ]
}

# Minimal screen1 for 2-screen setups.
screen1 = Screen(
    top=bar.Bar(
        [
            widget.WindowName(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                foreground=theme["white"],
                background=theme["BG4"],
                center_aligned=True,
                max_chars=20,
                **powerline,
                ),
            widget.Spacer(
                background=theme["BG4"],
                **powerline,
            ),
            widget.CurrentLayout(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                foreground=theme["green"],                         
                background=theme["background"],
                **powerline,
            ),
        ],
        size=25
    ),
    bottom=bar.Bar(
        [
            widget.GroupBox2(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                active=theme["green"],
                highlight_method="default",
                padding_x=8,
                #padding_y=8,
                foreground=theme["foreground"],                         
                background=theme["BG"],
                **powerline,
                ),
            widget.Prompt(),
            widget.WindowTabs(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                foreground=theme["white"],
                background=theme["BG4"],
                center_aligned=True,
                max_chars=40,
                **powerline,
                ),
        ],
        size=25,
    ),
)

# Primary screen for 1-screen setups, right screen for 2-screen setups.
screen2 = Screen(
    top=bar.Bar(
        [
            widget.WindowName(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                foreground=theme["white"],
                background=theme["BG4"],
                center_aligned=True,
                max_chars=20,
                **powerline,
                ),
            widget.Spacer(
                background=theme["BG4"],
                **powerline,
            ),
            widget.TextBox(
                f"ip: {local_ip}",
                name="default",
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                foreground=theme["foreground"],                         
                background=theme["background"],
                **powerline,
                ),
            widget.CurrentLayout(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                foreground=theme["green"],                         
                background=theme["background"],
                **powerline,
            ),
            widget.UPowerWidget(
                background=theme["BG2"],
                **powerline,
            ),
            widget.WiFiIcon(
                background=theme["BG2"],
                interface='wlp0s20f3',
                **powerline,
            ),
            widget.Bluetooth(
                background=theme["BG2"],
                **powerline,
            ),
            widget.Systray(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                background=theme["BG2"],
                icon_size=20,
                padding=5,
                **powerline
            ),
        ],
        size=25
    ),
    bottom=bar.Bar(
        [
            widget.GroupBox2(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                active=theme["green"],
                highlight_method="default",
                padding_x=8,
                #padding_y=8,
                foreground=theme["foreground"],                         
                background=theme["BG"],
                **powerline,
                ),
            widget.Prompt(),
            widget.WindowTabs(
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                foreground=theme["white"],
                background=theme["BG4"],
                center_aligned=True,
                max_chars=40,
                **powerline,
                ),
            widget.Clock(
                format='%Y-%m-%d %a %I:%M %p',
                fontsize=14,
                font="FiraCode Nerd Font Regular",
                foreground=theme["green"],                         
                background=theme["BG"],
                **powerline,
            ),
        ],
        size=25,
    ),
)

# Add screens.
screens = []
if NUM_SCREENS == 1:
    screens.append(screen2)
else:
    screens.append(screen1)
    screens.append(screen2)

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"


# Detect certain window names that should be floating.
@hook.subscribe.client_new
def float_display(win):
    wm_class = win.window.get_wm_class()
    w_name = win.window.get_name()
    if wm_class == ("display", "Display"):
        win.floating = True

def run(cmdline):
    logger.info("Running: %s" % cmdline)
    subprocess.Popen(shlex.split(cmdline))


@hook.subscribe.startup_once
def autostart():
    auto = osp.expanduser('~/.config/qtile/autostart.sh')
    run(auto)


@hook.subscribe.startup
def startup():
    """
    Run after qtile is started or reloaded.
    """
    logger.info("Qtile startup...")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Qtile system log: ~/.local/share/qtile/qtile.log")
    logger.info(f"NUM_SCREENS={NUM_SCREENS}")
    logger.info(f"HOME={os.environ['HOME']}")
    logger.info(f"DISPLAY={os.environ['DISPLAY']}")
    logger.info(f"VIRTUAL_ENV={os.environ['VIRTUAL_ENV']}")
    logger.info(f"PATH={os.environ['PATH']}")

    # Write the logging tree to a file.
    with open(".config/qtile/logging_tree.txt", 'w') as f:
        f.write(logging_tree.format.build_description())


@hook.subscribe.startup_once
def startup_init():
    """
    Run after qtile is started initially.
    """
    #run('xrandr --output DP1 --primary --mode 1920x1080 --rate 60.00 --output DP2 --mode 1920x1080 --rate 60.00 --right-of DP1')
    
    run('feh --bg-scale {}'.format(osp.join(HOME, '.config/qtile/wallpaper/iceland.jpg')))
