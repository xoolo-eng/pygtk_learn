"""Generation app."""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import (
    Gtk,
    # Gio,
    # GLib,
    # Gdk
)
from random import randint, sample
from colors import color
from threading import Lock


class Canvas(Gtk.DrawingArea):
    """."""

    SIZE_POINT = 10
    LINE_WIDTH = 0.1

    def __init__(self):
        """."""
        self.init = False
        super(Canvas, self).__init__()
        self.data = list()
        self.width = 0
        self.height = 0
        self.max_w = 0
        self.max_h = 0
        self.barriers_data = list()
        self.use_colors = {
            "background": "Green",
            "barier": "Grey",
            "bot": "DarkBlue"
        }
        self.mutex = Lock()
        self.params = dict()
        self.connect("draw", self.on_draw)

    def on_draw(self, canvas, cr):
        """."""
        cr.set_line_width(self.LINE_WIDTH)
        self.__draw_area(cr)
        self.__draw_bariers(cr)
        allocation = self.get_allocation()
        self.width = allocation.width // self.SIZE_POINT * self.SIZE_POINT
        self.height = allocation.height // self.SIZE_POINT * self.SIZE_POINT
        self.max_w = self.width // self.SIZE_POINT
        self.max_h = self.height // self.SIZE_POINT
        self.__create_bariers(5, 20)

    def __draw_area(self, cr):
        """."""
        cr.save()
        cr.set_source_rgb(*color("White"))
        cr.rectangle(0, 0, self.width, self.height)
        cr.fill()
        for x in range(
                0, self.width,
                self.SIZE_POINT):
            for y in range(
                    0, self.height,
                    self.SIZE_POINT):
                cr.move_to(
                    x+self.LINE_WIDTH,
                    y+self.LINE_WIDTH
                )
                cr.rectangle(
                    x+self.LINE_WIDTH,
                    y+self.LINE_WIDTH,
                    self.SIZE_POINT-self.LINE_WIDTH,
                    self.SIZE_POINT-self.LINE_WIDTH
                )
        cr.set_source_rgb(*color(self.use_colors["background"]))
        cr.fill()
        cr.restore()

    def __create_bariers(self, count, length):
        """."""
        start_x = sample(range(self.max_w), count)
        start_y = sample(range(self.max_h), count)
        directions = list()
        for i in range(count):
            directions.append([
                tuple([start_x[i], start_y[i]-1]),
                tuple([start_x[i]+1, start_y[i]]),
                tuple([start_x[i], start_y[i]+1]),
                tuple([start_x[i]-1, start_y[i]])
            ])
        # print(directions)
        self.barriers_data = list()
        self.mutex.acquire()
        try:
            for i in range(count):
                self.barriers_data.append({tuple([start_x[i], start_y[i]])})
            for i in range(count):
                print(i)
                for j in range(length-1):
                    direction = randint(0, 3)
                    print(direction, list(self.barriers_data[i])[-1])
                    new_x, new_y = directions[i][direction]
                    curent_x, curent_y = list(self.barriers_data[i])[-1]
                    if not (0 <= new_x < self.max_w):
                        new_x = curent_x
                    if not (0 <= new_y < self.max_h):
                        new_y = curent_y
                    self.barriers_data[i].add(tuple([new_x, new_y]))
                    if direction == 0:
                        directions[i][0] = tuple([new_x, new_y-1])
                    elif direction == 1:
                        directions[i][1] = tuple([new_x+1, new_y])
                    elif direction == 2:
                        directions[i][2] = tuple([new_x, new_y+1])
                    elif direction == 3:
                        directions[i][3] = tuple([new_x-1, new_y])
        finally:
            self.mutex.release()
        print(self.barriers_data)

    def __draw_bariers(self, cr):
        """."""
        cr.save()
        for barier_coords in self.barriers_data:
            for coords in list(barier_coords):
                self.__rectangle(cr, coords, self.use_colors["barier"])
        cr.restore()

    def __rectangle(self, cr, coords, color_name):
        """."""
        cr.save()
        cr.set_source_rgb(*color(color_name))
        cr.move_to(
            (coords[0]*self.SIZE_POINT),
            (coords[1]*self.SIZE_POINT)
        )
        cr.rectangle(
            (coords[0]*self.SIZE_POINT),
            (coords[1]*self.SIZE_POINT),
            self.SIZE_POINT,
            self.SIZE_POINT
        )
        cr.fill()
        cr.restore()

    def set_data(self, data=[]):
        """."""
        self.params = dict()
        self.params["clean"] = True
        self.data = data
        self.queue_draw()


class DrawingWindow(Gtk.Window):
    """."""

    def __init__(self):
        """."""
        super(Gtk.Window, self).__init__(title="DrawingArea")
        self.__create_interface()
        self.energy = 0

    def __create_interface(self):
        """Create interface."""
        self.set_size_request(600, 400)
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

        execute_button = Gtk.Button("Start")
        execute_button.connect("clicked", self.on_execute)
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
        self.energy_s_button.connect("changed", self.on_changed_energy)
        right_box.pack_start(self.energy_s_button, False, True, 0)

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

        button_box = Gtk.ButtonBox()
        right_box.pack_start(button_box, False, True, 0)

        self.apply_energy_button = Gtk.Button("Apply")
        self.apply_energy_button.set_sensitive(False)
        self.apply_energy_button.connect("clicked", self.on_apply_energy)
        button_box.add(self.apply_energy_button)

        close_button = Gtk.Button("Close")
        close_button.connect("clicked", Gtk.main_quit)
        button_box.add(close_button)

        self.canvas = Canvas()
        left_box.pack_start(self.canvas, True, True, 0)

    def on_execute(self, button):
        """Run Imitation."""
        print("on_execute()")
        self.canvas.set_data([])

    def on_changed_energy(self, spin):
        """Change lavel energy."""
        if self.energy == spin.get_value_as_int():
            self.apply_energy_button.set_sensitive(False)
        else:
            self.apply_energy_button.set_sensitive(True)
        print(spin.get_value_as_int())

    def on_apply_energy(self, widget):
        """Apply energy."""
        self.energy = self.energy_s_button.get_value_as_int()
        widget.set_sensitive(False)
        print("Apply energy")


if __name__ == '__main__':
    win = DrawingWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
