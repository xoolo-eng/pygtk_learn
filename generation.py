"""Generation app."""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import (
    Gtk,
    # Gio,
    # GLib,
    # Gdk
)
from random import randint, sample, choice
from colors import color
from threading import Lock
from collections import namedtuple


Coords = namedtuple("Coords", ["x", "y"])


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


class WorkPlace():

    def __init__(self, **kwargs):
        self.size_point = kwargs.get("size_point", 5)
        self.width_line = kwargs.get("width_line", 0.1)
        self.count_bariers = kwargs.get("conut_bariers", 5)
        self.maxlen_barier = kwargs.get("maxlen_barier", 50)
        self.count_food = kwargs.get("count_food", 50)
        self.persent_poison = kwargs.get("persent_poison", 20)
        self.__barriers_data = list()
        self.__food_data = list()
        self.__poison_data = list()
        self.reload = True

    def get_bariers(self, *args):
        if self.reload:
            max_x, max_y = args
            start_x = sample(range(max_x), self.count_bariers)
            start_y = sample(range(max_y), self.count_bariers)
            directions = list()
            for i in range(self.count_bariers):
                directions.append([
                    Coords(start_x[i], start_y[i]-1),
                    Coords(start_x[i]+1, start_y[i]),
                    Coords(start_x[i], start_y[i]+1),
                    Coords(start_x[i]-1, start_y[i])
                ])
            self.__barriers_data = list()
            bariers = list()
            for i in range(self.count_bariers):
                bariers.append(Coords(start_x[i], start_y[i]))
                self.__barriers_data.append(Coords(start_x[i], start_y[i]))
            for i in range(self.count_bariers):
                old_direction = randint(0, 3)
                for j in range(self.maxlen_barier-1):
                    direction = randint(0, 9)
                    if direction > old_direction:
                        direction = old_direction
                    old_direction = direction
                    new_x, new_y = directions[i][direction]
                    curent_x, curent_y = bariers[i]
                    if not (0 <= new_x < max_x):
                        new_x = curent_x
                    if not (0 <= new_y < max_y):
                        new_y = curent_y
                    bariers[i] = (Coords(new_x, new_y))
                    if direction == 0:
                        directions[i][0] = Coords(new_x, new_y-1)
                        directions[i][1] = Coords(new_x+1, new_y)
                        directions[i][3] = Coords(new_x-1, new_y)
                    elif direction == 1:
                        directions[i][0] = Coords(new_x, new_y-1)
                        directions[i][1] = Coords(new_x+1, new_y)
                        directions[i][2] = Coords(new_x, new_y+1)
                    elif direction == 2:
                        directions[i][1] = Coords(new_x+1, new_y)
                        directions[i][2] = Coords(new_x, new_y+1)
                        directions[i][3] = Coords(new_x-1, new_y)
                    elif direction == 3:
                        directions[i][0] = Coords(new_x, new_y-1)
                        directions[i][2] = Coords(new_x, new_y+1)
                        directions[i][3] = Coords(new_x-1, new_y)
                    self.__barriers_data.append(Coords(new_x, new_y))
            if self.__barriers_data and self.__food_data and self.__poison_data:
                self.reload = False
        return self.__barriers_data

    def get_food(self, *args):
        if self.reload:
            max_x, max_y = args
            self.__food_data = list()
            for _ in range(self.count_food):
                while True:
                    coords = Coords(
                        randint(0, max_x-1),
                        randint(0, max_y-1)
                    )
                    if coords not in self.__barriers_data:
                        self.__food_data.append(coords)
                        break
            if self.__barriers_data and self.__food_data and self.__poison_data:
                self.reload = False
        return self.__food_data

    def get_poison(self):
        if self.reload:
            self.__poison_data = list()
            count = int(len(self.__food_data) / 100 * self.persent_poison)
            for i in range(count):
                while True:
                    element = choice(self.__food_data)
                    if element not in self.__poison_data:
                        self.__poison_data.append(element)
                        break
            if self.__barriers_data and self.__food_data and self.__poison_data:
                self.reload = False
        return self.__poison_data

    def set_reload(self):
        self.__barriers_data = list()
        self.__food_data = list()
        self.__poison_data = list()
        self.reload = True


class Canvas(Gtk.DrawingArea):
    """."""

    SIZE_POINT = 10  #
    LINE_WIDTH = 0.1  #

    def __init__(self, *args, **kwargs):
        """."""
        super(Canvas, self).__init__()
        self.data = list()
        # ###
        # allocation = self.get_allocation()
        # self.width = allocation.width // self.SIZE_POINT * self.SIZE_POINT
        # self.height = allocation.height // self.SIZE_POINT * self.SIZE_POINT
        # self.max_w = self.width // self.SIZE_POINT
        # self.max_h = self.height // self.SIZE_POINT
        # ###
        self.work_place = WorkPlace(
            size_point=self.SIZE_POINT,
            width_line=self.LINE_WIDTH
        )
        # self.barriers_data = self.work_place.get_bariers(self.max_w, self.max_h)
        # self.food_data = self.work_place.get_food(self.max_w, self.max_h)
        # self.poison_data = self.work_place.get_poison()
        # self.bots_data = list()
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
        self.barriers_data = self.work_place.get_bariers(
            self.max_w, self.max_h
        )
        self.food_data = self.work_place.get_food(
            self.max_w, self.max_h
        )
        self.poison_data = self.work_place.get_poison()
        self.bots_data = list()

        cr.set_line_width(self.LINE_WIDTH)
        self.__draw_area(cr)
        self.__draw_barriers(cr)
        self.__draw_food(cr)

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

    def __draw_barriers(self, cr):
        """."""
        cr.save()
        for coords in self.barriers_data:
            self.__rectangle(cr, coords, self.use_colors["barier"])
        cr.restore()

    def __draw_food(self, cr):
        """."""
        cr.save()
        for coords in self.food_data:
            if coords not in self.poison_data:
                self.__rectangle(cr, coords, self.use_colors["food"])
            else:
                self.__rectangle(cr, coords, self.use_colors["poison"])
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

    def set_data(self, data):
        """."""
        if data:
            self.work_place.set_reload()
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

        self.scroll_box = Gtk.ScrolledWindow()
        self.scroll_box.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        left_box.pack_start(self.scroll_box, True, True, 0)

        self.canvas = Canvas()
        self.scroll_box.add(self.canvas)

        allocation = self.get_allocation()
        self.WIDTH = allocation.width
        self.HEIGTH = allocation.height

    def on_execute(self, button):
        """Run Imitation."""
        self.canvas.set_data(False)

    def on_changed_energy(self, spin):
        """Change lavel energy."""
        if self.energy == spin.get_value_as_int():
            self.apply_energy_button.set_sensitive(False)
        else:
            self.apply_energy_button.set_sensitive(True)

    def on_apply_energy(self, widget):
        """Apply energy."""
        self.energy = self.energy_s_button.get_value_as_int()
        widget.set_sensitive(False)
        self.canvas.set_data(True)


if __name__ == '__main__':
    win = DrawingWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
