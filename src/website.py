from random import randint
from room import Room

class Site:
    def __init__(self):
        self.active_rooms = {}    # Room code to Player object
        self.active_players = {}  # Player name to room code
        self.sid_username = {}    # Player sid to username

    def contains_user(self, user):
        return user in self.active_players
    
    def contains_user_id(self, user_id):
        return user_id in self.sid_username
    
    def add_user(self, user, user_sid):
        self.active_players[user] = -1 # In no room
        self.sid_username[user_sid] = user

    def remove_user_id(self, user_id):
        user = self.sid_username[user_id]
        room_code = self.active_players[user]

        if room_code != -1: # In a room
            self.remove_player_from_room(room_code, user)
        
        del self.active_players[user]
        del self.sid_username[user_id]
        return room_code

    def create_room(self, host_id):
        while (room_code := str(randint(100000, 999999))) in self.active_rooms:
            pass
        host = self.sid_username[host_id]
        self.active_rooms[room_code] = Room(host, host_id)
        self.active_players[host] = room_code
        return room_code

    def remove_room(self, room_code):
        try:
            assert(self.num_players_in_room(room_code) == 0)
        except:
            print(f"Cannot remove room {room_code} because it isn't empty")
        else:
            del self.active_rooms[room_code]

    def is_valid_room(self, room_code):
        return room_code in self.active_rooms
    
    def add_player_to_room(self, room_code, player_id):
        player_name = self.sid_username[player_id]
        self.active_rooms[room_code].add_player(player_name, player_id)
        self.active_players[player_name] = room_code

    def remove_player_from_room(self, room_code, player_name):
        self.active_rooms[room_code].remove_player(player_name)
        self.active_players[player_name] = -1
        self.remove_room(room_code)

    def is_room_host(self, room_code, host):
        return self.active_rooms[room_code].host == host
    
    def is_room_active(self, room_code):
        return self.active_rooms[room_code].active
    
    def num_players_in_room(self, room_code):
        return self.active_rooms[room_code].num_players_in_room()
    
    def set_up_room(self, room_code):
        self.active_rooms[room_code].set_up()

    def make_player_move(self, room_code, player_name, guess, time):
        return self.active_rooms[room_code].player_guess(player_name, guess, time)
    
    def get_room_leaderboard(self, room_code):
        return self.active_rooms[room_code].leaderboard()
    
    def get_player_guesses(self, room_code, player_name):
        return self.active_rooms[room_code].get_player_guesses(player_name)
    
    def get_player_keyboard(self, room_code, player_name):
        return self.active_rooms[room_code].get_player_keyboard(player_name)
    
    def get_room_word(self, room_code):
        return self.active_rooms[room_code].word
