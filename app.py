from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from src.website import Site


app = Flask(__name__)
socketio = SocketIO(app)
site = Site()

@app.route("/", methods=["GET"])
def load():
    return render_template("index.html")

@socketio.on("login_user")
def login_user(data_json):
    username = data_json["username"]
    if site.contains_user(username):
        socketio.emit("invalid", {"error": f"Username {username} is taken"}, to=request.sid)
    else:
        site.add_user(username, request.sid)
        socketio.emit("login_valid_username", {"username": username}, to=request.sid)

@socketio.on("new_room")
def new_room():
    room_code = site.create_room(request.sid)
    join_room(room_code)
    socketio.emit("room_valid", {"room_code": room_code, "room_players": site.num_players_in_room(room_code)}, to=room_code)

@socketio.on("join_room")
def join_room_user(data_json):
    room_code = data_json["room_code"]

    if site.is_valid_room(room_code):
        if not site.is_room_active(room_code):
            site.add_player_to_room(room_code, request.sid)
            join_room(room_code)
            socketio.emit("room_valid", {"room_code": room_code, "room_players": site.num_players_in_room(room_code)}, to=room_code)
        else:
            socketio.emit("invalid", {"error": f"Room {room_code} is currently active"}, to=request.sid)
    else:
        socketio.emit("invalid", {"error": f"Room {room_code} does not exist"}, to=request.sid)

@socketio.on("start_game")
def start_game(data_json):
    username = data_json["username"]
    room_code = data_json["room_code"]

    if site.is_room_host(room_code, username):
        if not site.is_room_active(room_code):
            site.set_up_room(room_code)
            socketio.emit("game_load", {"keyboard": site.get_player_keyboard(room_code, username)}, to=room_code)
        else:
            socketio.emit("invalid", {"error": f"Room {room_code} is currently active"}, to=request.sid)
    else:
        socketio.emit("invalid", {"error": f"{username} is not the host of room {room_code}"}, to=request.sid)

@socketio.on("game_guess")
def game_guess(data_json):
    username = data_json["username"]
    room_code = data_json["room_code"]
    guess = data_json["game_guess"]
    time = data_json["time"]

    done = site.make_player_move(room_code, username, guess, time)
    if done:
        ret_ids, leaderboard = site.get_room_leaderboard(room_code)
        for id in ret_ids:
            socketio.emit("end_page", {"correct_word": site.get_room_word(room_code), "leaderboard": leaderboard}, to=id)
    else:
        guesses = site.get_player_guesses(room_code, username)
        if guesses[-1] == "WND":
            guesses.pop()
            socketio.emit("invalid", {"error": f"{guess} is not in the Dictionary"}, to=request.sid)
        else:
            socketio.emit("game_valid_guess", {"guesses": guesses, "keyboard": site.get_player_keyboard(room_code, username)}, to=request.sid)

@socketio.on("disconnect")
def disconnect():
    if site.contains_user_id(request.sid):
        room_code = site.remove_user_id(request.sid)
        if room_code != -1:
            leave_room(room_code)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")