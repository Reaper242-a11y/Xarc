#!/usr/bin/env python3

import gi
import os

gi.require_version("Gtk", "4.0")
gi.require_version("Vte", "3.91")

from gi.repository import Gdk, Gtk, Vte, GLib


APP_ID = "com.newhorizon.xarc-terminal"
VERSION = "0.2.0"


class XarcTerminal(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id=APP_ID,
            flags=0
        )

def do_activate(self):
	window = Gtk.ApplicationWindow(application=self)

	 window.set_title("Xarc Terminal")
 	window.set_default_size(1000, 650)

	terminal = Vte.Terminal()

def paste_action(widget,args):
 terminal.paste_clipboard()
 return True

shortcut = Gtk.ShortcutController()

trigger = Gtk.ShortcutTrigger.parse_string("<Control><Shift>V")
action = Gtk.CallbackAction.new(paste_action)

shortcut.add_shortcut(
	Gtk.Shortcut.new(trigger, action)
)

terminal.add_controller(shortcut)

terminal.set_scrollback_lines(10000)

terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.path.expanduser("~"),
            ["/bin/zsh"],
            None,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None,
        )

 window.set_child(terminal)

window.present()


def main():
    app = XarcTerminal()
    app.run()


if __name__ == "__main__":
    main()
