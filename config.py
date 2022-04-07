# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile.widget import TextBox

from libqtile.layout.columns import Columns
from libqtile.layout.xmonad import MonadTall
from libqtile.layout.stack import Stack
from libqtile.layout.floating import Floating

from libqtile.extension.dmenu import DmenuRun
from colors import nord_fox, gruvbox
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
#    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.run_extension(DmenuRun(
        font="JETBRAINS MONO",
        font_size="13",
        dmenu_command="dmenu_run",
        dmenu_prompt=">_",
        background= nord_fox["bg"],
        foreground=nord_fox["gray"],
        selected_foreground=nord_fox["cyan"],
        selected_background=nord_fox["bg"]
    ))),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    MonadTall(
        border_normal="#8991a1",
        border_focus="#6a7790",
        margin=5,
        border_width=1,
        single_border_width=1,
        single_margin=1,
    ),

    Stack(
        border_normal="#8991a1",
        border_focus="#6a7790",
        border_width=1,
        num_stacks=1,
        margin=0,
    ),
]
widget_defaults = dict(
    font="TerminessTTF Nerd Font",
    fontsize=14,
    padding=10,
)
extension_defaults = widget_defaults.copy()

def lower_left_triangle(bg_color, fg_color):
    return TextBox(
        text=' ',
        padding=0,
        fontsize=50,
        background=bg_color,
        foreground=fg_color)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    text=" "
                ),
                widget.GroupBox(
                    borderwidth=0,
                    active=nord_fox['white'],
                    inactive=nord_fox['white'],
                    disable_drag=True,
                    block_highlight_text_color=nord_fox['white'],
                    highlight_color=nord_fox['cyan'],
                    highlight_method='line',
                ),

                lower_left_triangle(nord_fox['bg'], nord_fox['magenta']),
                widget.CurrentLayout(
                    background=nord_fox['magenta'],
                ),

                lower_left_triangle(nord_fox['magenta'], nord_fox['blue']),
                widget.WindowCount(
                    background=nord_fox['blue'],
                    show_zero=True,
                ),

                lower_left_triangle(nord_fox['blue'], nord_fox['bg']),
                widget.Prompt(),
                widget.WindowName(),

                lower_left_triangle(nord_fox['bg'], nord_fox['light_nord']),
                widget.CPU(
                    background=nord_fox['light_nord'],
                    format=' {freq_current}GHz {load_percent}%',
                    foreground=nord_fox['magenta']
                ),
                widget.Memory(
                    background=nord_fox['light_nord'],
                    foreground=nord_fox['yellow'],
                    format=" {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}"
                ),
                widget.Net(
                    background=nord_fox['light_nord'],
                    format="{down}  {up}",
                    foreground=nord_fox['green']
                ),
                widget.Clock(
                    background=nord_fox['light_nord'],
                    format="  %Y-%m-%d %a %I:%M %p",
                    foreground=nord_fox['red']
                ),
                lower_left_triangle(nord_fox['light_nord'], nord_fox['light_nord']),
                # lower_left_triangle(nord_fox['bg'], nord_fox['magenta']),
                widget.Systray(
                    background=nord_fox['light_nord'],
                ),

                lower_left_triangle(nord_fox['light_nord'], nord_fox['bg']),
                widget.Spacer(
                    background=nord_fox['bg'],
                    length=10
                )
            ],
            background=nord_fox['bg'],
            size=24,
            opacity=1,
            # margin=[10, 10, 5, 10],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
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
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])
