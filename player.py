
class Player:

    def __init__(self, color: str) -> None:
        if color == "w":
            self.color = color
            self.opponent_color = "b"
        else:
            self.color = "b"
            self.opponent_color = "w"
        self.choice = None
        self.bear_off = False
        self.winner = False


    def select_move(self, moves_indexes):
        self.choice = None
        options = {index: move for index, move in enumerate(moves_indexes)}
        player_choice = None
        while player_choice not in options:
            try:
                player_choice = int(input(f"Player {self.color} move {options}: "))
                self.choice = options[player_choice]
            except ValueError:
                print("Wrong choice. ValueError.")
                continue
            except KeyError:
                print("Wrong choice. KeyError.")
                continue
