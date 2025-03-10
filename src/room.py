import os
from src.game import Game
from src.player import Player
from typing import List, Union, Tuple

class Room: # Room class
    def __init__(self, host: str, host_id: str) -> None:
        """
        Initialize a Room object
        """
        self.word = None
        self.host = host
        self.players = {host: Player(host, host_id)}
        self.game = Game(os.path.join(os.path.dirname(__file__), "words.txt"))
        self.active = 0

    def add_player(self, player_name: str, player_id: str) -> None:
        """
        Add a new player to the current room
        """
        self.players[player_name] = Player(player_name, player_id)

    def remove_player(self, player_name: str) -> None:
        """
        Remove the player from the current room (when they disconnect)
        """
        if not self.players[player_name].done:
            self.active -= 1
            
        del self.players[player_name]
        if player_name == self.host:
            if self.num_players_in_room() != 0: # Not empty room - find another host
                self.host = list(self.players.keys())[0]

    def num_players_in_room(self) -> int:
        """
        Returns the number of players currently in the room
        """
        return len(self.players)
    
    def set_up(self) -> None:
        """
        Setup the game for every player in the room by resetting their attributes and randomly selecting a word for the current round
        """
        self.word = self.game.generate_game_word()
        for player in self.players.values():
            player.reset()
        self.active = len(self.players)

    def player_guess(self, player_name: str, guess: str, time: str) -> bool:
        """
        Process the player's guess and update their attributes
        
        Returns:
            bool indicating if the player has guessed the word/used up their 6 guesses (used to switch to end_page)
        """
        if self.word:
            res = self.game.run_guess(guess, self.word)
            ret = self.players[player_name].update_after_guess(res, time)
            if ret:
                self.active -= 1
            return ret
        else:
            raise Exception
    
    def leaderboard(self) -> Tuple[List[str], List[Tuple[str, bool, int, float]]]:
        """
        Generates a leaderboard for the room based on player performance

        Returns:
            A list of player session IDs (`ret_ids`).
            A sorted list of tuples (`ret_leaderboard`), where each tuple contains (sorted in order of Solved > Num Guesses > Time Taken):
                - Player name (str)
                - Solved status (bool)
                - Number of guesses (int)
                - Time taken (float)
        """
        ret_leaderboard = []
        ret_ids = []
        for value in self.players.values():
            if value.done:
                ret_leaderboard.append((value.name, value.completed, len(value.guesses), value.time))
                ret_ids.append(value.sid)

        ret_leaderboard.sort(key=lambda item: (not item[1], item[2], item[3]))
        self.active = len(ret_leaderboard) != len(self.players)
        return ret_ids, ret_leaderboard
    
    def get_player_guesses(self, player_name: str) -> List[Union[List[List[Union[str, int]]], str]]:
        """
        Return a list of the player's guesses and their results this round
        """
        return self.players[player_name].guesses
    
    def get_player_keyboard(self, player_name: str) -> List[List[List[Union[str, int]]]]:
        """
        Return the characters used by the player and their status this round
        """
        return self.players[player_name].keyboard
