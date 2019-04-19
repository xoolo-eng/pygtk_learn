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
from collections import namedtuple


Coords = namedtuple("Coords", ["x", "y"])
# class Coords():
#     """."""
#
#     def __init__(self, x, y):
#         """."""
#         self.__x = x
#         self.__y = y
#
#     def __getattr__(self, name):
#         """Сделать в виде дескрипторов."""
#         if name not in ["x", "y"]:
#             raise AttributeError
#         return self.__dict__[f"_Coords__{name}"]
#
#     def __iter__(self):
#         """."""
#         self.__result = self.__generator()
#         return self
#
#     def __next__(self):
#         """."""
#         try:
#             result = next(self.__result)
#         except Exception:
#             raise StopIteration
#         else:
#             return result
#
#     def __generator(self):
#         yield self.__x
#         yield self.__y


class Bot():
    """."""

    def __init__(self, coords):
        """."""
        self.genom = list()
        self.__init_genom()
        self.x, self.y = coords

    def __init_genom(self):
        """."""
        for i in range(64):
            self.genom.append(randint(0, 63))


class Canvas(Gtk.DrawingArea):
    """."""

    SIZE_POINT = 5
    LINE_WIDTH = 0.1

    def __init__(self, *args, **kwargs):
        """."""
        super(Canvas, self).__init__()
        self.data = list()
        self.width = 0
        self.height = 0
        self.max_w = 0
        self.max_h = 0
        self.barriers_data = list()
        self.food_data = list()
        self.poison_data = list()
        self.bots_data = list()
        self.use_colors = {
            "background": "LightGray",
            "barier": "Gray",
            "bot": "DarkBlue",
            "food": "Green",
            "poison": "DarkRed"
        }
        self.mutex = Lock()
        self.params = dict()
        self.connect("draw", self.on_draw)

    def on_draw(self, canvas, cr):
        """."""
        allocation = self.get_allocation()
        self.width = allocation.width // self.SIZE_POINT * self.SIZE_POINT
        self.height = allocation.height // self.SIZE_POINT * self.SIZE_POINT
        self.max_w = self.width // self.SIZE_POINT
        self.max_h = self.height // self.SIZE_POINT
        if self.params.get("draw"):
            cr.set_line_width(self.LINE_WIDTH)
            self.__draw_area(cr)
            self.__draw_bariers(cr)
            self.__draw_food(cr)
        else:
            self.__create_bariers(5, 50)
            self.__create_food(200)
            self.params["draw"] = True

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
                Coords(start_x[i], start_y[i]-1),
                Coords(start_x[i]+1, start_y[i]),
                Coords(start_x[i], start_y[i]+1),
                Coords(start_x[i]-1, start_y[i])
            ])
        self.barriers_data = list()
        bariers = list()
        self.mutex.acquire()
        try:
            for i in range(count):
                bariers.append(Coords(start_x[i], start_y[i]))
                self.barriers_data.append(Coords(start_x[i], start_y[i]))
            for i in range(count):
                for j in range(length-1):
                    direction = randint(0, 3)
                    new_x, new_y = directions[i][direction]
                    curent_x, curent_y = bariers[i]
                    if not (0 <= new_x < self.max_w):
                        new_x = curent_x
                    if not (0 <= new_y < self.max_h):
                        new_y = curent_y
                    bariers[i] = (Coords(new_x, new_y))
                    if direction == 0:
                        directions[i][0] = Coords(new_x, new_y-1)
                    elif direction == 1:
                        directions[i][1] = Coords(new_x+1, new_y)
                    elif direction == 2:
                        directions[i][2] = Coords(new_x, new_y+1)
                    elif direction == 3:
                        directions[i][3] = Coords(new_x-1, new_y)
                    self.barriers_data.append(Coords(new_x, new_y))
        finally:
            self.mutex.release()

    def __draw_bariers(self, cr):
        """."""
        cr.save()
        for coords in self.barriers_data:
            self.__rectangle(cr, coords, self.use_colors["barier"])
        cr.restore()

    def __create_food(self, count):
        """."""
        self.food_data = list()
        for i in range(count):
            while True:
                coords = Coords(randint(0, self.max_w-1), randint(0, self.max_h-1))
                if coords not in self.barriers_data:
                    self.food_data.append(coords)
                    break

    def __draw_food(self, cr):
        """."""
        cr.save()
        for coords in self.food_data:
            self.__rectangle(cr, coords, self.use_colors["food"])
        cr.restore()

    def __rectangle(self, cr, coords, color_name):
        """."""
        cr.save()
        cr.set_source_rgb(*color(color_name))
        cr.rectangle(
            (coords.x * self.SIZE_POINT) + self.LINE_WIDTH,
            (coords.y * self.SIZE_POINT) + self.LINE_WIDTH,
            self.SIZE_POINT - self.LINE_WIDTH,
            self.SIZE_POINT - self.LINE_WIDTH
        )
        cr.fill()
        cr.restore()

    def set_data(self, data=[]):
        """."""
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

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

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

        separator = Gtk.HSeparator()
        right_box.pack_start(separator, False, True, 10)

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
