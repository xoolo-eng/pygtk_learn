from random import randint, choice
from tools import Coords


class Bot():

    curent_bot = 0
    directions = [
        ("top", None, 0),
        ("top", "right", 1),
        ("right", None, 2),
        ("right", "bottom", 3),
        ("bottom", None, 4),
        ("bottom", "left", 5),
        ("left", None, 6),
        ("left", "top", 7),
    ]

    def __init__(self, **kwargs):
        self.genom = self.__init_genom() if kwargs.get("new") else list()
        self.x, self.y = kwargs.get("coords", (0, 0))
        self.energy = kwargs.get("energy", 200)
        self.direction = randint(0, 7)
        self.cursor = 0

    def __init_genom(self):
        genom = list()
        for i in range(64):
            genom.append(randint(0, 63))
        return genom

    def get_coords(self):
        return Coords(self.x, self.y)

    def set_coords(self, coords):
        self.x, self.y = coords

    def get_child(self, mutatuin=False):
        new_bot = Bot(
            coords=(self.x, self.y)
        )
        new_bot.genom = self.genom.copy()
        if mutatuin:
            new_bot.genom[randint(0, 63)] = randint(0, 63)
        return new_bot

    def __move(self, directions, *args):
        print(id(self), directions, "look")
        def check(value, max):
            if 0 <= value < max:
                return value
            elif 0 > value:
                return 0
            elif max == value:
                return max - 1
            else:
                print("ERROR")

        __directions = {
            "top": (lambda x, y: (x, check(y - 1, args[1]))),
            "right": (lambda x, y: (check(x + 1, args[0]), y)),
            "bottom": (lambda x, y: (x, check(y + 1, args[1]))),
            "left": (lambda x, y: (check(x - 1, args[0]), y))
        }
        # if direction not in __directions:
        #     raise ValueError(f"Direction can will be in {__directions} only")
        # else:
        self.x, self.y = __directions[directions[0]](self.x, self.y)
        if directions[1] is not None:
            self.x, self.y = __directions[directions[1]](self.x, self.y)
        return self.__energy()

    def __turn(self, directions, *args):
        self.direction = directions[2]
        print(id(self), directions, "turn")
        return self.__energy()

    def __look(self, directions, *args):
        print(id(self), directions, "look")
        pass

    def __food(self, directions, *args):
        print(id(self), directions, "food")
        pass

    def __energy(self):
        if self.energy > 0:
            self.energy -= 1
            return True
        else:
            return False

    def __step(self, *args):
        self.curent_bot = id(self)
        real_cursor = ((self.cursor % 8) + self.direction) % 8
        print(id(self), self.direction)
        action_direction = self.directions[real_cursor]
        if 0 <= self.genom[self.cursor] < 16:
            # Выполнение завершающей команды
            if 0 <= self.genom[self.cursor] < 8:
                # move
                self.__move(action_direction, *args)
                # if action_direction[1]:
                #     self.__move(action_direction[1])

            if 8 <= self.genom[self.cursor] < 16:
                # turn
                self.__turn(action_direction, *args)
                # if action_direction[1]:
                #     self.__turn(action_direction[1])

            self.curent_bot = 0
            # return
        if 16 <= self.genom[self.cursor] < 32:
            # Выполнение не завершающейго действия
            if 16 <= self.genom[self.cursor] < 24:
                # look
                self.__look(action_direction, *args)
                # if action_direction[1]:
                #     self.__look(action_direction[1])

            if 24 <= self.genom[self.cursor] < 32:
                # food
                self.__food(action_direction, *args)
                # if action_direction[1]:
                #     self.__food(action_direction[1])

            # return
        if 32 <= self.genom[self.cursor] < 64:
            # Безусловный переход
            self.cursor = self.genom[self.cursor]
            self.curent_bot = 0
            # return
        self.cursor = (self.cursor + 1) if self.cursor < 63 else 0

    def action(self, *args):
        if self.curent_bot != 0:
            if self.curent_bot == id(self):
                self.__step(*args)
            else:
                return
        else:
            self.__step(*args)


if __name__ == '__main__':

    def get_coords(*args):
        coords = Coords(
            randint(0, args[0]-1),
            randint(0, args[1]-1)
        )
        return coords

    bots = [
        Bot(
            new=True,
            coords=get_coords(200, 400)
        ) for _ in range(5)
    ]
    print([bot.get_coords() for bot in bots])
    for bot in bots:
        bot.action()
    print([bot.get_coords() for bot in bots])
    for bot in bots:
        bot.action()
    print([bot.get_coords() for bot in bots])
    for bot in bots:
        bot.action()
    print([bot.get_coords() for bot in bots])
