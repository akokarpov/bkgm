
from random import randint


class Dice:

    def __init__(self) -> None:
        self.rolled_dices = []

    def roll_dices(self):
        self.rolled_dices = []
        for _ in range(2):
            dice = randint(1, 6)
            if dice in self.rolled_dices:
                self.rolled_dices = [dice, dice, dice, dice]
            else:
                self.rolled_dices.append(dice)
        print(f"Dices: {self.rolled_dices}")
        return self.rolled_dices
