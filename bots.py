from random import randint, choice
from tools import Coords


class Bot():

    curent_bot = 0
    directions = [
        ("top", None),
        ("top", "right"),
        ("right", None),
        ("right", "bottom"),
        ("bottom", None),
        ("bottom", "left"),
        ("left", None),
        ("left", "top"),
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

    def __move(self, direction):

        def check(value, min, max):
            if min <= value < max:
                return value
            elif min > value:
                return min
            elif max < value:
                return max

        min, max = (0, 400)
        directions = {
            "top": (lambda x, y: (x, check(y - 1, min, max))),
            "right": (lambda x, y: (check(x + 1, min, max), y)),
            "bottom": (lambda x, y: (x, check(y + 1, min, max))),
            "left": (lambda x, y: (check(x - 1, min, max), y))
        }
        if direction not in directions:
            raise ValueError(f"Direction can will be in {directions} only")
        else:
            self.x, self.y = directions[direction](self.x, self.y)
            return self.__energy()

    def __turn(self, directions):
        self.direction = directions[2]

    def __look(self, directions):
        pass

    def __food(self, directions):
        pass

    def __energy(self):
        if self.energy > 0:
            self.energy -= 1
            return True
        else:
            return False

    def __step(self):
        self.curent_bot = id(self)
        real_cursor = ((self.cursor % 8) + self.direction) % 8
        self.cursor += 1
        action_direction = self.directions[real_cursor]
        if 0 <= self.cursor < 16:
            # Выполнение завершающей команды
            if 0 <= self.cursor < 8:
                pass  # move
                self.__move(action_direction[0])
                if action_direction[1]:
                    self.__move(action_direction[1])

            if 8 <= self.cursor < 16:
                pass  # turn
                self.__turn(action_direction[0])
                if action_direction[1]:
                    self.__turn(action_direction[1])

            self.curent_bot = 0
            return
        if 16 <= self.cursor < 32:
            # Выполнение не завершающейго действия
            if 16 <= self.cursor < 24:
                pass  # look
                self.__look(action_direction[0])
                if action_direction[1]:
                    self.__look(action_direction[1])

            if 24 <= self.cursor < 32:
                pass  # food
                self.__food(action_direction[0])
                if action_direction[1]:
                    self.__food(action_direction[1])

            return
        if 32 <= self.cursor < 64:
            # Безусловный переход
            self.cursor = self.genom[self.cursor]
            self.curent_bot = 0
            return

    def action(self):
        if self.curent_bot:
            if self.curent_bot == id(self):
                self.__step()
            else:
                return
        else:
            self.__step()


if __name__ == '__main__':
    bot = Bot(
        new=True,
        coords=(10, 16),
        energy=200
    )
    print(bot.get_coords())
    bot.move("bottom")
    print(bot.get_coords())
    first_bot = bot.get_child()
    for i in range(200):
        first_bot.move(choice(["top", "right", "bottom", "left"]))
        print(first_bot.get_coords())
