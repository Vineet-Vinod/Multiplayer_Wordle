import socket
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from src.webserver import Server
from typing import List, Union, Tuple, Dict


app = Flask(__name__)
socketio = SocketIO(app)
server = Server()

@app.route("/", methods=["GET"])
def load() -> str:
    """
    Return the HTML template in index.html
    """
    return render_template("index.html")

@socketio.on("login_user")
def login_user(data_json: Dict[str, str]) -> None:
    """
    Log the user into the server if their username is not taken
    Else, ask them to choose a different username
    """
    username = data_json["username"]
    if server.contains_user(username):
        socketio.emit("invalid", {"error": f"Username {username} is taken"}, to=request.sid)
    else:
        server.add_user(username, request.sid)
        socketio.emit("login_valid_username", {"username": username}, to=request.sid)

@socketio.on("new_room")
def new_room() -> None:
    """
    Create a new room with the user as its host
    """
    room_code = server.create_room(request.sid)
    join_room(room_code)
    socketio.emit("room_valid", {"room_code": room_code, "room_players": server.num_players_in_room(room_code)}, to=room_code)

@socketio.on("join_room")
def join_room_user(data_json: Dict[str, str]) -> None:
    """
    Add the user to the room if it exists and is not active
    Else, respond with the appropriate error message
    """
    room_code = data_json["room_code"]

    if server.is_valid_room(room_code):
        if not server.is_room_active(room_code):
            server.add_player_to_room(room_code, request.sid)
            join_room(room_code)
            socketio.emit("room_valid", {"room_code": room_code, "room_players": server.num_players_in_room(room_code)}, to=room_code)
        else:
            socketio.emit("invalid", {"error": f"Room {room_code} is currently active"}, to=request.sid)
    else:
        socketio.emit("invalid", {"error": f"Room {room_code} does not exist"}, to=request.sid)

@socketio.on("start_game")
def start_game(data_json: Dict[str, str]) -> None:
    """
    Start the round in the room if the host pressed "Start"
    Else, indicate that only the host can start a round
    """
    username = data_json["username"]
    room_code = data_json["room_code"]

    if server.is_room_host(room_code, username):
        if not server.is_room_active(room_code):
            server.set_up_room(room_code)
            socketio.emit("game_load", {"keyboard": server.get_player_keyboard(room_code, username)}, to=room_code)
        else:
            socketio.emit("invalid", {"error": f"Room {room_code} is currently active"}, to=request.sid)
    else:
        socketio.emit("invalid", {"error": f"{username} is not the host of room {room_code}"}, to=request.sid)

@socketio.on("game_guess")
def game_guess(data_json: Dict[str, str]) -> None:
    """
    Process the player's guess and switch to the correct next state depending on the result
    1. Not a valid word - error message and allow the player to guess again
    2. Guessed correctly - go to end page (solved = True)
    3. Guessed incorrectly (less than 6 guesses) - report used characters' status and allow the player to guess again
    4. Guessed incorrectly and 6 guesses - go to end page (solved = False)
    """
    username = data_json["username"]
    room_code = data_json["room_code"]
    guess = data_json["game_guess"]
    time = data_json["time"]

    done = server.make_player_move(room_code, username, guess, time)
    if done:
        ret_ids, leaderboard = server.get_room_leaderboard(room_code)
        for id in ret_ids:
            socketio.emit("end_page", {"correct_word": server.get_room_word(room_code), "leaderboard": leaderboard}, to=id)
    else:
        guesses = server.get_player_guesses(room_code, username)
        if guesses[-1] == "WND":
            guesses.pop()
            socketio.emit("invalid", {"error": f"{guess} is not in the Dictionary"}, to=request.sid)
        else:
            socketio.emit("game_valid_guess", {"guesses": guesses, "keyboard": server.get_player_keyboard(room_code, username)}, to=request.sid)

@socketio.on("disconnect")
def disconnect() -> None:
    """
    Handle server side clean up when player disconnects (page reload/close)
    """
    if server.contains_user_id(request.sid):
        room_code = server.remove_user_id(request.sid)
        if room_code != -1:
            leave_room(room_code)


if __name__ == "__main__":
    print("Starting server...")
    print(f"Play on: http://{socket.gethostbyname(socket.gethostname())}:5000")
    socketio.run(app, host="0.0.0.0", port=5000)