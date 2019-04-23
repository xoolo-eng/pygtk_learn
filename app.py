from window import DrawingWindow
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import (
    Gtk,
    # Gio,
    # GLib,
    # Gdk
)

win = DrawingWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
