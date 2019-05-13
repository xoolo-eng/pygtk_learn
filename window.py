"""Generation app."""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from canvas import Canvas


class DrawingWindow(Gtk.Window):

    def __init__(self):
        super(Gtk.Window, self).__init__(title="DrawingArea")
        self.energy = 200
        self.__create_interface()

    def __create_interface(self):
        self.maximize()
        self.set_position(Gtk.WindowPosition.CENTER)

        box_master = Gtk.Box()
        box_master.set_border_width(5)
        self.add(box_master)

        left_box = Gtk.Box()
        box_master.pack_start(left_box, True, True, 0)

        separator = Gtk.VSeparator()
        box_master.pack_start(separator, False, False, 5)

        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_box.set_size_request(150, -1)
        box_master.add(right_box)

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

        execute_button = Gtk.ToggleButton("Start")
        execute_button.set_active(False)
        execute_button.connect("toggled", self.on_execute)
        right_box.pack_start(execute_button, False, True, 0)

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

        label = Gtk.Label("Count bots")
        right_box.pack_start(label, False, True, 0)
        self.count_bots_entry = Gtk.Entry()
        self.count_bots_entry.set_text(str(0))
        self.count_bots_entry.set_editable(False)
        right_box.pack_start(self.count_bots_entry, False, True, 0)

        label = Gtk.Label("Generation")
        right_box.pack_start(label, False, True, 0)
        self.generation_entry = Gtk.Entry()
        self.generation_entry.set_text(str(0))
        self.generation_entry.set_editable(False)
        right_box.pack_start(self.generation_entry, False, True, 0)

        label = Gtk.Label("Mutatuins")
        right_box.pack_start(label, False, True, 0)
        self.mutation_entry = Gtk.Entry()
        self.mutation_entry.set_text(str(0))
        self.mutation_entry.set_editable(False)
        right_box.pack_start(self.mutation_entry, False, True, 0)

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

        space = Gtk.Alignment()
        right_box.pack_start(space, True, True, 0)

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

        label = Gtk.Label("Energy")
        right_box.pack_start(label, False, True, 0)
        self.energy_s_button = Gtk.SpinButton()
        adjuctment = Gtk.Adjustment(0.0, 0.0, 1000.0, 10.0, 50.0, 0.0)
        self.energy_s_button.set_adjustment(adjuctment)
        self.energy_s_button.set_value(self.energy)
        self.energy_s_button.connect("changed", self.on_changed_energy)
        right_box.pack_start(self.energy_s_button, False, True, 0)

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

        button_box = Gtk.ButtonBox()
        right_box.pack_start(button_box, False, True, 0)

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

        self.apply_energy_button = Gtk.Button("Apply")
        self.apply_energy_button.set_sensitive(False)
        self.apply_energy_button.connect("clicked", self.on_apply_energy)
        button_box.add(self.apply_energy_button)

        close_button = Gtk.Button("Close")
        close_button.connect("clicked", Gtk.main_quit)
        button_box.add(close_button)

        self.scroll_box = Gtk.ScrolledWindow()
        self.scroll_box.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        left_box.pack_start(self.scroll_box, True, True, 0)

        self.canvas = Canvas(
            energy=self.energy
        )
        self.scroll_box.add(self.canvas)

    def on_execute(self, button):
        if button.get_active():
            # self.canvas.run()
            # self.__timeout_id = GLib.timeout_add(10, self.on_start, self)
            self.__timeout_id = GLib.timeout_add(100, self.on_start, self)
            button.set_label("Stop")
        else:
            # self.canvas.stop()
            GLib.source_remove(self.__timeout_id)
            del self.__timeout_id
            button.set_label("Start")

    def on_changed_energy(self, spin):
        if self.energy == spin.get_value_as_int():
            self.apply_energy_button.set_sensitive(False)
        else:
            self.apply_energy_button.set_sensitive(True)

    def on_apply_energy(self, widget):
        self.energy = self.energy_s_button.get_value_as_int()
        widget.set_sensitive(False)
        self.canvas.set_data(True)

    def on_start(self, widget):
        widget.canvas.queue_draw()
        return True
