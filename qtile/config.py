#   ___ _____ ___ _     _____    ____             __ _       
#  / _ \_   _|_ _| |   | ____|  / ___|___  _ __  / _(_) __ _ 
# | | | || |  | || |   |  _|   | |   / _ \| '_ \| |_| |/ _` |
# | |_| || |  | || |___| |___  | |__| (_) | | | |  _| | (_| |
#  \__\_\|_| |___|_____|_____|  \____\___/|_| |_|_| |_|\__, |
#                                                      |___/ 

# Icons: https://fontawesome.com/search?o=r&m=free

import os
import subprocess
import json
from libqtile import hook
from libqtile import qtile
from typing import List  
from libqtile import bar, layout
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Backlight
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder
from pathlib import Path
from libqtile.log_utils import logger
import iwlib # type: ignore

from qtile_extras import widget # type: ignore
from qtile_extras.widget.decorations import RectDecoration # type: ignore
from qtile_extras.widget.decorations import PowerLineDecoration # type: ignore
import qtile_extras.hook # type: ignore
from qtile_extras.popup.templates.mpris2 import COMPACT_LAYOUT, DEFAULT_LAYOUT

# --------------------------------------------------------
# Your configuration
# --------------------------------------------------------

# Keyboard layout in autostart.sh

# Show bluetooth status bar widget
show_bluetooth = True
# show_bluetooth = False

# --------------------------------------------------------
# General Variables
# --------------------------------------------------------

# Get home path
home = str(Path.home())
volume = 0
volume_increment = 5

# --------------------------------------------------------
# Custom Functions
# --------------------------------------------------------

@lazy.function
def maximize_by_switching_layout(qtile):
    current_layout_name = qtile.current_group.layout.name
    if current_layout_name == 'columns':
        qtile.current_group.layout = 'max'
    elif current_layout_name == 'max':
        qtile.current_group.layout = 'columns'


# --------------------------------------------------------
# Check for Desktop/Laptop
# --------------------------------------------------------

# 3 = Desktop
platform = int(os.popen("cat /sys/class/dmi/id/chassis_type").read())

# --------------------------------------------------------
# Set default apps
# --------------------------------------------------------

terminal     = "kitty"        
browser      = "firefox"
launcher     = "rofi -show drun"
file_manager = "dolphin"

# --------------------------------------------------------
# Keybindings
# --------------------------------------------------------

mod   = "mod4" # Windows key
left  = "h"
down  = "j"
up    = "k"
right = "l"

keys = [
    # Focus
    Key([mod], left, lazy.layout.left(), desc="Move focus to left"),
    Key([mod], right, lazy.layout.right(), desc="Move focus to right"),
    Key([mod], down, lazy.layout.down(), desc="Move focus down"),
    Key([mod], up, lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window around"),
    
    # Move
    Key([mod, "shift"], left, lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], right, lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], down, lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], up, lazy.layout.shuffle_up(), desc="Move window up"),

    # Swap
    Key([mod, "shift", "control"], left, lazy.layout.swap_column_left()),
    Key([mod, "shift", "control"], right, lazy.layout.swap_column_right()),

    # Key([mod], "Print", lazy.spawn(home + "/dotfiles/qtile/scripts/screenshot.sh")),

    # Size
    Key([mod, "control"], down, lazy.layout.grow_down(), desc="Grow window downwards"),
    Key([mod, "control"], up, lazy.layout.grow_up(), desc="Grow window upwards"),
    Key([mod, "control"], left, lazy.layout.grow_left()),
    Key([mod, "control"], right, lazy.layout.grow_right()),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Floating
    Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),
    
    # Mode
    Key([mod], "s", lazy.layout.toggle_split(), desc="Swap between split or stacked for current column"),

    # Toggle Layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    # Fullscreen
    Key([mod], "f", maximize_by_switching_layout()),

    #System
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "r", lazy.reload_config(), desc="Reload the config"),
    # Key([mod, "control"], "q", lazy.spawn(home + "/dotfiles/qtile/scripts/powermenu.sh"), desc="Open Powermenu"),

    # Apps
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "control"], "Return", lazy.spawn(launcher), desc="Launch Rofi"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "d", lazy.spawn(file_manager), desc="Launch file manager"),

    Key([mod], "equal", lazy.spawn("brightnessctl -q s +20%"), desc="Brightness += 20%"),
    Key([mod], "minus", lazy.spawn("brightnessctl -q s 20%-"), desc="Brightness -= 20%"), 

    # VOLUME
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-")),
]

# --------------------------------------------------------
# Groups
# --------------------------------------------------------

groups = [Group(i, layout='columns') for i in "123456789"]

dgroups_key_binder = simple_key_binder(mod)

# Add keybind where mod+scroll wheel switches

# --------------------------------------------------------
# Scratchpads
# --------------------------------------------------------

groups.append(ScratchPad("scratchpad", [
    DropDown("terminal", terminal, x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
]))

keys.extend([
    Key([mod], 'F1', lazy.group["scratchpad"].dropdown_toggle("terminal")),
])

groups.append(ScratchPad("scratchpad", [
    DropDown("keepassxc", "keepassxc", x=0.3, y=0.1, width=0.4, height=0.4, on_focus_lost_hide=False),
]))

keys.extend([
    Key([mod], 'F2', lazy.group["scratchpad"].dropdown_toggle("keepassxc"))
])

# Not functional
groups.append(ScratchPad("scratchpad", [
    DropDown("htop", "htop", x=0.3, y=0.1, width=0.4, height=0.4, on_focus_lost_hide=False),
]))

keys.extend([
    Key([mod], 'F3', lazy.group["scratchpad"].dropdown_toggle("htop"))
])
# --------------------------------------------------------
# Colors
# --------------------------------------------------------

Color0 = "#3d2146" # deep purple
Color1 = "#ff7bef" # bright pink
Color2 = "#b3fbf7" # cyan
Color3 = "#2c2f4a" # dark blue
Color4 = "#4e1f4c" # bright purple
Color5 = "#f4c4d1" # hot pink
Color6 = "#89568d" # greyish purple
Color7 = "#e17b66" # orange
Color8 = "#202020"
Color9 = "#050505.45" # Bar background

# --------------------------------------------------------
# Setup Layout Theme
# --------------------------------------------------------

layout_theme = { 
    "border_width": 1,
    "margin": 0,
    "border_focus": Color6,
    #"border_normal": Color8,
    "single_border_width": 2
}

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layouts = [
    layout.Columns(**layout_theme,),
    layout.Max(**layout_theme,),
]

# --------------------------------------------------------
# Setup Widget Defaults
# --------------------------------------------------------
widget_defaults = dict(
    font="Fira Sans SemiBold",
    fontsize=11,
    padding=5
)
extension_defaults = widget_defaults.copy()

# --------------------------------------------------------
# Widgets
# --------------------------------------------------------
powerline = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding_y=5, radius=0),
        PowerLineDecoration(path="rounded_left", padding_y=5)
    ]
}

decoration_group = {
    "decorations": [
        RectDecoration(color=Color2, radius=10, filled=True, padding_y=4, padding_x=10, group = False)
    ],
    "padding": 20,
}

widget_list = [
    widget.CurrentLayout(
        **decoration_group
    ),
    widget.GroupBox(
        highlight_method='text',
        this_current_screen_border=Color1,
        hide_unused=True,
        **decoration_group
    ),
    widget.Memory(
        measure_mem='G',
        format="Memory: {MemPercent}%",
        **decoration_group
    ),
    widget.CPU(
        format="CPU: {load_percent}%",
        **decoration_group
    ),
    widget.NvidiaSensors(
       format='GPU: {temp}°C',
       **decoration_group
    ),
    widget.Net(
        **decoration_group
    ),
    widget.Spacer(),
    widget.Systray(
        icon_size=20,
    ),
    widget.DF(
        warn_space=400, # Only show if available space is below 400G
        partition='/home',
        **decoration_group
    ),
    widget.DF(
        warn_space=5,
        partition='/',
        **decoration_group
    ),
    widget.CheckUpdates(
        distro='Arch_checkupdates',
        update_interval=60, # Check every 60 seconds
        display_format='Outdated Packages: {updates}',
        execute='kitty --dump-commands yay',
        **decoration_group
    ),
    widget.Wlan(
        format='{essid} {percent:2.0%}',
        **decoration_group
    ),
    widget.Clock(
        format="%d/%m/%y %H:%M",
        **decoration_group
    ),
    widget.Volume(
        fmt="Volume: {}",
        **decoration_group
    ),
]


# Hide Modules if not on laptop

# --------------------------------------------------------
# Screens
# --------------------------------------------------------
screens = [
    Screen(
        top=bar.Bar(
            widget_list,
            30, # Height
            padding=0,
            opacity=1,
            border_width=[0, 0, 0, 0],
            margin=[0,0,0,0],
            background="#000000.0"
        ),
    ),
]
# --------------------------------------------------------
# Drag floating layouts
# --------------------------------------------------------

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# --------------------------------------------------------
# Define floating layouts
# --------------------------------------------------------

floating_layout = layout.Floating(
    border_width=4,
    border_focus=Color4,
    border_normal="FFFFFF",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

# --------------------------------------------------------
# General Setup
# --------------------------------------------------------

dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

# --------------------------------------------------------
# Windows Manager Name
# --------------------------------------------------------

wmname = "QTILE"

# --------------------------------------------------------
# Hooks
# --------------------------------------------------------

# HOOK startup
@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([script])
