""" Current running party config """


class Config:
    def __init__(self):
        self.difficulty = 1  # Easy
        self.mode = 1  # Dark
        self.player_name = ''

    def set_mode(self, mode):
        self.mode = mode

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def set_player_name(self, name):
        self.player_name = name

    def get_mode(self):
        return self.mode

    def get_difficulty(self):
        return self.difficulty

    def get_difficulty_display_name(self):
        if self.difficulty == 1:
            return 'Easy'
        elif self.difficulty == 2:
            return 'Hard'
        else:
            return 'Impossible'

    def get_player_name(self):
        return self.player_name
