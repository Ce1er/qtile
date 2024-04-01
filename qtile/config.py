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

mod   = "mod1" # ALT KEY
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
    Key([mod, "shift"], left, lazy.layout.swap_left()),
    Key([mod, "shift"], right, lazy.layout.swap_right()),

    # Key([mod], "Print", lazy.spawn(home + "/dotfiles/qtile/scripts/screenshot.sh")),

    # Size
    Key([mod, "control"], down, lazy.layout.shrink(), desc="Grow window to the left"),
    Key([mod, "control"], up, lazy.layout.grow(), desc="Grow window to the right"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Floating
    Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),
    
    # Split
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),

    # Toggle Layouts
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),

    # Fullscreen
    Key([mod], "f", lazy.window.toggle_fullscreen()),

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
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -D pulse sset Master 5%+")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -D pulse sset Master 5%-")),
]

# --------------------------------------------------------
# Groups
# --------------------------------------------------------

groups = [Group(i, layout='monadtall') for i in "123456789"]

dgroups_key_binder = simple_key_binder(mod)

# --------------------------------------------------------
# Scratchpads
# --------------------------------------------------------

groups.append(ScratchPad("scratchpad", [
    DropDown("terminal", terminal, x=0.3, y=0.1, width=0.40, height=0.4, on_focus_lost_hide=False ),
]))

keys.extend([
    Key([mod], 'F1', lazy.group["scratchpad"].dropdown_toggle("terminal")),
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
    "border_width": 2,
    "margin": 10,
    "border_focus": Color6,
    #"border_normal": Color8,
    "single_border_width": 2
}

# --------------------------------------------------------
# Layouts
# --------------------------------------------------------

layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating()
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
widget_list = [
        widget.GroupBox(
        background=Color9,
        highlight_method='block',
        highlight='ffffff',
        block_border='ffffff',
        highlight_color=['ffffff','ffffff'],
        block_highlight_text_color='000000',
        foreground='ffffff',
        rounded=False,
        this_current_screen_border='ffffff',
        active='ffffff'
    ),
    widget.WindowName(
        max_chars=50,
        background=Color9,
        width=400,
        padding=10
    ),
    widget.Spacer(
        background=Color9
    ),
    widget.TextBox(
        background=Color9      
    ),    
    widget.Memory(
        background=Color9,
        padding=10,        
        measure_mem='G',
        format="Memory: {MemPercent}%" # SWAP
    ),
    widget.CPU(
        padding=10, 
        background=Color9,        
        visible_on_warn=False,
        format="CPU: {load_percent}%"
    ),
    widget.Volume(
        background=Color9,
        padding=10, 
        fmt='Volume: {}',
    ),
    widget.BrightnessControl(
        background=Color9,
        padding=10,
        mode="bar"
    ),
    widget.ThermalZone(
            background=Color9,
            padding=10,
            crit=70,
            format="temp}°C"
    ),
    widget.Clock(
        background=Color9,   
        padding=10,      
        format="%Y-%m-%d / %I:%M %p",
    ),
    widget.StatusNotifier(
            background=Color9,
            padding=10,
            icon_size=16,
            icon_theme=None,
            mouse_callbacks={}
    ),
    widget.UPowerWidget(
            background=Color9,
            padding=10,
            fill_charge="a6d608",
            fill_critical="cc0000",
            fill_low="aa00aa",
            fill_normal="dbdbe0",
            format="{percentage}% {tte} until empty"
    ),
    widget.WiFiIcon(
            background=Color9,
            padding=5,
            active_color="ffffff",
            inactive_colour="a5a5a5",
            update_interval=1,
            disconnected_colour="aa0000",
            check_connection_interval=1,
            interface="wlan0"

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
            padding=20,
            opacity=1,
            border_width=[0, 0, 0, 0],
            margin=[0,0,0,0],
            background="#000000.3"
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
auto_minimize = True

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

@qtile_extras.hook.subscribe.up_battery_low
def battery_low(battery_name):
    send_notification(battery_name, "Battery is running low.")

@qtile_extras.hook.subscribe.up_battery_critical
def battery_critical(battery_name):
    send_notification(battery_name, "Battery is critically low.")
