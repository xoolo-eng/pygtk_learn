"""Canvas."""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from random import randint, sample, choice
from colors import color
from threading import Lock
from bots import Bot
from tools import Coords, COUNT_BOTS


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
        self.bots = list()

    def create_bots(self, *args):
        if not self.bots:
            self.bots = [
                Bot(
                    new=True,
                    coords=self.get_coords(*args)
                ) for _ in range(COUNT_BOTS)
            ]

    def get_bariers(self, *args):
        if not self.__barriers_data:
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
        return self.__barriers_data

    def get_food(self, *args):
        if not self.__food_data:
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
        return self.__food_data

    def get_poison(self):
        if not self.__poison_data:
            self.__poison_data = list()
            count = int(len(self.__food_data) / 100 * self.persent_poison)
            for i in range(count):
                while True:
                    element = choice(self.__food_data)
                    if element not in self.__poison_data:
                        self.__poison_data.append(element)
                        break
        return self.__poison_data

    def set_reload(self):
        self.__barriers_data = list()
        self.__food_data = list()
        self.__poison_data = list

    def get_coords(self, *args):
        while True:
            coords = Coords(
                randint(0, args[0]-1),
                randint(0, args[1]-1)
            )
            if coords in self.__barriers_data:
                continue
            if coords in self.__food_data:
                continue
            return coords

    def step(self):
        for bot in self.bots:
            bot.action()


class Canvas(Gtk.DrawingArea):

    SIZE_POINT = 10  #
    WIDTH_LINE = 0.1  #

    def __init__(self, **kwargs):
        super(Canvas, self).__init__()
        self.data = list()
        self.work_place = WorkPlace(
            size_point=kwargs.get("size_point", self.SIZE_POINT),
            width_line=kwargs.get("width_line", self.WIDTH_LINE),
            count_food=kwargs.get("energy", 0)
        )
        self.use_colors = {
            "background": "LightGray",
            "barier": "DarkGray",
            "bot": "DarkBlue",
            "food": "Green",
            "poison": "DarkRed"
        }
        self.mutex = Lock()
        self.connect("draw", self.on_draw)

    def on_draw(self, canvas, cr):
        allocation = self.get_allocation()
        self.width = allocation.width // self.SIZE_POINT * self.SIZE_POINT
        self.height = allocation.height // self.SIZE_POINT * self.SIZE_POINT
        max_w = self.width // self.SIZE_POINT
        max_h = self.height // self.SIZE_POINT
        self.barriers_data = self.work_place.get_bariers(
            max_w, max_h
        )
        self.food_data = self.work_place.get_food(
            max_w, max_h
        )
        self.poison_data = self.work_place.get_poison()
        self.work_place.create_bots(max_w, max_h)

        cr.set_line_width(self.WIDTH_LINE)
        self.__draw_area(cr)
        self.__draw_barriers(cr)
        self.__draw_food(cr)
        self.__draw_bots(cr)

    def __draw_area(self, cr):
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
                    x+self.WIDTH_LINE,
                    y+self.WIDTH_LINE,
                    self.SIZE_POINT-self.WIDTH_LINE,
                    self.SIZE_POINT-self.WIDTH_LINE
                )
        cr.set_source_rgb(*color(self.use_colors["background"]))
        cr.fill()
        cr.restore()

    def __draw_barriers(self, cr):
        cr.save()
        for coords in self.barriers_data:
            self.__rectangle(cr, coords, self.use_colors["barier"])
        cr.restore()

    def __draw_food(self, cr):
        cr.save()
        for coords in self.food_data:
            if coords not in self.poison_data:
                self.__rectangle(cr, coords, self.use_colors["food"])
            else:
                self.__rectangle(cr, coords, self.use_colors["poison"])
        cr.restore()

    def __draw_bots(self, cr):
        cr.save()
        for coords in self.data:
            self.__rectangle(cr, coords, self.use_colors["bot"])
        cr.restore()
        self.work_place.step()

    def __rectangle(self, cr, coords, color_name):
        cr.save()
        cr.set_source_rgb(*color(color_name))
        cr.rectangle(
            (coords.x * self.SIZE_POINT) + self.WIDTH_LINE,
            (coords.y * self.SIZE_POINT) + self.WIDTH_LINE,
            self.SIZE_POINT - self.WIDTH_LINE,
            self.SIZE_POINT - self.WIDTH_LINE
        )
        cr.fill()
        cr.restore()

    def re_draw(self):
        self.data = [bot.get_coords() for bot in self.work_place.bots]
        self.queue_draw()
