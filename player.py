""" Module to store player information """


class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score

    def increment_score(self):
        self.score += 1
