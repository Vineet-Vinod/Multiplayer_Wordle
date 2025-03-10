import os
from src.game import Game
from src.player import Player

class Room: # Room class
    def __init__(self, host, host_id):
        self.word = None
        self.host = host
        self.players = {host: Player(host, host_id)}
        self.game = Game(os.path.join(os.path.dirname(__file__), "words.txt"))
        self.active = False

    def add_player(self, player_name, player_id):
        self.players[player_name] = Player(player_name, player_id)

    def remove_player(self, player_name):
        del self.players[player_name]
        if player_name == self.host:
            if self.num_players_in_room() != 0: # Not empty room - find another host
                self.host = list(self.players.keys())[0]

    def num_players_in_room(self):
        return len(self.players)
    
    def set_up(self):
        self.word = self.game.generate_game_word()
        for player in self.players.values():
            player.reset()
        self.active = True

    def player_guess(self, player_name, guess, time):
        res = self.game.run_guess(guess, self.word)
        return self.players[player_name].update_after_guess(res, time)
    
    def leaderboard(self):
        ret_leaderboard = []
        ret_ids = []
        for value in self.players.values():
            if value.done:
                ret_leaderboard.append((value.name, value.completed, len(value.guesses), value.time))
                ret_ids.append(value.sid)

        ret_leaderboard.sort(key=lambda item: (not item[1], item[2], item[3])) # Completed > Num Guesses > Time taken
        self.active = len(ret_leaderboard) != len(self.players)
        return ret_ids, ret_leaderboard
    
    def get_player_guesses(self, player_name):
        return self.players[player_name].guesses
    
    def get_player_keyboard(self, player_name):
        return self.players[player_name].keyboard
