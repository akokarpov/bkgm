
from settings import Settings


class Player:
    """Player class which represents a human or CPU."""

    def __init__(self, color, screen) -> None:
        self.settings = Settings()
        self.screen = screen
        if color == "w":
            self.color = color
            self.opponent_color = "b"
        else:
            self.color = "b"
            self.opponent_color = "w"
        self.bear_off = False
        self.winner = False
        self.cpu = False

    def get_label(self):
        """Return a text label to blit on screen."""
        name = "CPU" if self.cpu else "Player"
        if self.bear_off:
            label = f"{name} '{self.color.upper()}' is bearing off..."
        else:
            label = f"{name} '{self.color.upper()}' is making a move..."
        if self.winner:
            label = f"{name} '{self.color.upper()}' has won the game."
        return self.settings.font.render(label, True, self.settings.BLACK)

    def blitme(self):
        """Draws text heading who's turn it is on screen."""
        self.screen.blit(self.get_label(), ((self.settings.WIDTH - self.settings.back_width) / 2, 8))
