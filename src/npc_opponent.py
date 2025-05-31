import random

class NPC:
    def __init__(self):
        self.name = "NPC Opponent"
        self.score = 0
        self.level = 1

    def make_move(self, game_state):
        # Simple random move for now
        moves = ["left", "right", "down", "rotate"]
        return random.choice(moves)

    def update_score(self, points):
        self.score += points