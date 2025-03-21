from random import randint
from src.room import Room
from typing import List, Union, Tuple, Dict

class Server: # Singleton Class
    __instance = None

    def __new__(cls) -> "Server":
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        """
        Initialize the webserver
        """
        self.active_rooms: Dict[str, Room] = {}    # Room code to Room object
        self.active_players: Dict[str, str] = {}   # Player name to room code
        self.sid_username: Dict[str, str] = {}     # Player sid to name

    def contains_user(self, user: str) -> bool:
        """
        Return if the username is taken
        """
        return user in self.active_players
    
    def contains_user_id(self, user_id: str) -> bool:
        """
        Return if the userid is online
        """
        return user_id in self.sid_username
    
    def add_user(self, user: str, user_sid: str) -> None:
        """
        Add the user to the server
        """
        self.active_players[user] = -1 # In no room
        self.sid_username[user_sid] = user

    def remove_user_id(self, user_id: str) -> Union[str, int]:
        """
        Remove the user_id from the server (clean up when the user disconnects)

        Returns:
            str - their current room
            -1 if they aren't in a room
        """
        user = self.sid_username[user_id]
        room_code = self.active_players[user]

        if room_code != -1: # In a room
            self.remove_player_from_room(room_code, user)
        
        del self.active_players[user]
        del self.sid_username[user_id]
        return room_code

    def create_room(self, host_id: str) -> str:
        """
        Create a room with a unique room_code and add the host_id as the host

        Returns:
            str - room_code
        """
        while (room_code := str(randint(100000, 999999))) in self.active_rooms:
            pass
        host = self.sid_username[host_id]
        self.active_rooms[room_code] = Room(host, host_id)
        self.active_players[host] = room_code
        return room_code

    def remove_room(self, room_code: str) -> None:
        """
        Remove the room from the server when all players in the room disconnect
        """
        try:
            assert(self.num_players_in_room(room_code) == 0)
        except:
            pass
        else:
            del self.active_rooms[room_code]

    def is_valid_room(self, room_code: str) -> bool:
        """
        Return if the room exists in the server
        """
        return room_code in self.active_rooms
    
    def add_player_to_room(self, room_code: str, player_id: str) -> None:
        """
        Add player_id to room_code
        """
        player_name = self.sid_username[player_id]
        self.active_rooms[room_code].add_player(player_name, player_id)
        self.active_players[player_name] = room_code

    def remove_player_from_room(self, room_code: str, player_name: str) -> None:
        """
        Remove player_id from room_code
        """
        self.active_rooms[room_code].remove_player(player_name)
        self.active_players[player_name] = -1
        self.remove_room(room_code)

    def is_room_host(self, room_code: str, host: str) -> bool:
        """
        Return if host is the host of room_code (only hosts can start a round)
        """
        try:
            return self.active_rooms[room_code].host == host
        except:
            return False
    
    def is_room_active(self, room_code: str) -> bool:
        """
        Return if there is an active round in the room (players cannot join an active room)
        """
        try:
            return self.active_rooms[room_code].active
        except:
            return True
    
    def num_players_in_room(self, room_code: str) -> int:
        """
        Return the number of players currently in room_code
        """
        try:
            return self.active_rooms[room_code].num_players_in_room()
        except:
            return 0
    
    def set_up_room(self, room_code: str) -> None:
        """
        Set up room_code for the next round
        """
        try:
            self.active_rooms[room_code].set_up()
        except:
            pass

    def make_player_move(self, room_code: str, player_name: str, guess: str, time: str) -> bool:
        """
        Process the player's guess and update their attributes
        
        Returns:
            bool indicating if the player has guessed the word/used up their 6 guesses (used to switch to end_page)
        """
        try:
            return self.active_rooms[room_code].player_guess(player_name, guess, time)
        except:
            return False
    
    def get_room_leaderboard(self, room_code: str) -> Tuple[List[str], List[Tuple[str, bool, int, float]]]:
        """
        Returns room_code's leaderboard
        """
        return self.active_rooms[room_code].leaderboard()
    
    def get_player_guesses(self, room_code: str, player_name: str) -> List[Union[List[List[Union[str, int]]], str]]:
        """
        Returns player_name's guesses in the current round
        """
        try:
            return self.active_rooms[room_code].get_player_guesses(player_name)
        except:
            return ["ERR"]
    
    def get_player_keyboard(self, room_code: str, player_name: str) -> List[List[List[Union[str, int]]]]:
        """
        Returns player_name's keyboard (character usage)
        """
        try:
            return self.active_rooms[room_code].get_player_keyboard(player_name)
        except:
            return ["ERR"]
    
    def get_room_word(self, room_code: str) -> str:
        """
        Returns the current round word in room_code
        """
        return self.active_rooms[room_code].word
