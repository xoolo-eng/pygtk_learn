from random import randint, choice
from canvas import Coords


class Bot():

    def __init__(self, **kwargs):
        self.genom = self.__init_genom() if kwargs.get("new") else list()
        self.x, self.y = kwargs.get("coords", (0, 0))
        self.energy = kwargs.get("energy", 200)

    def __init_genom(self):
        genom = list()
        for i in range(64):
            genom.append(randint(0, 63))
        return genom

    def get_coords(self):
        return Coords(self.x, self.y)

    def get_child(self, mutatuin=False):
        new_bot = Bot(
            coords=(self.x, self.y)
        )
        new_bot.genom = self.genom.copy()
        if mutatuin:
            new_bot.genom[randint(0, 63)] = randint(0, 63)
        return new_bot

    def move(self, direction):

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

    def __energy(self):
        if self.energy > 0:
            self.energy -= 1
            return True
        else:
            return False

    def action():
        pass


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
