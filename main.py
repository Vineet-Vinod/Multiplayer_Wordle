from flask import Flask, redirect, url_for, render_template, request, session, flash
from random import randint
from datetime import timedelta
import time
from game import Game, Room


# Configure app
app = Flask(__name__)
app.secret_key = "vWordle"
app.permanent_session_lifetime = timedelta(minutes=10)

# Configure Wordle game
game = Game("words.txt")
active_room_codes = {}
active_players = set()


@app.route("/login", methods=["POST", "GET"])
def login():
    if "user" in session:
        return redirect(url_for("init"))
    
    else:
        if request.method == "POST":
            session.permanent = True
            user = request.form["name"]
            if user in active_players:
                flash(f"Username {user} is taken")
                return render_template("enter.html")

            session["user"] = user
            active_players.add(user)
            return redirect(url_for("init"))
        else:
            return render_template("enter.html")
    

@app.route("/", methods=["POST", "GET"])
def init():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        if request.form["button"] == "New Room":
            # Create new room, redirect to room
            room_code = str(randint(100000, 999999))
            # Need to figure out room deletion
            active_room_codes[room_code] = Room()
            return redirect(url_for("room", room_code=room_code))
        
        else:
            room_code = request.form["code"]
            if room_code in active_room_codes: # Valid room, redirect to room
                active_room_codes[room_code].players += 1
                return redirect(url_for("room", room_code=room_code))
            else: # Indicate no such room exists
                flash(f"Room {room_code} does not exist")
    
    return render_template("init.html")


@app.route("/room/<room_code>", methods=["POST", "GET"])
def room(room_code):
    if "user" not in session:
        return redirect(url_for("login"))
    
    if room_code not in active_room_codes:
        flash(f"Room {room_code} does not exist")
        time.sleep(1)
        return redirect(url_for("init"))
    
    if request.method == "POST":
        return redirect(url_for("setup", room_code=room_code))
    
    return render_template("room.html", room_code=room_code, players=active_room_codes[room_code].players)


@app.route("/setup/<room_code>")
def setup(room_code):
    if active_room_codes[room_code].word is None or len(active_room_codes[room_code].completed) == len(active_room_codes[room_code].player_times):
        active_room_codes[room_code].word = game.generate_game_word()

    active_room_codes[room_code].player_times[session["user"]] = time.time()
    active_room_codes[room_code].player_guesses[session["user"]].clear()
    active_room_codes[room_code].completed.clear()
    active_room_codes[room_code].round[session["user"]] += 1
    return redirect(url_for("play", room_code=room_code))


@app.route("/room/<room_code>/play", methods=["POST", "GET"])
def play(room_code):
    if "user" not in session:
        return redirect(url_for("login"))
    
    if room_code not in active_room_codes:
        flash(f"Room {room_code} does not exist")
        time.sleep(1)
        return redirect(url_for("init"))
    
    if request.method == "POST":
        res = game.run_guess(request.form["guess"], active_room_codes[room_code].word)
        if res == "Word not in dictionary":
            flash(res)
        else:
            active_room_codes[room_code].player_guesses[session["user"]].append(res)
            vals = active_room_codes[room_code].player_guesses[session["user"]]
            if len(vals) == 6 or (vals and vals[-1] == "Correct, you solved it!"):
                active_room_codes[room_code].completed[session["user"]] = ((vals and vals[-1] == "Correct, you solved it!"), round(time.time() - active_room_codes[room_code].player_times[session["user"]], 3))
                vals.append(f"The word was {active_room_codes[room_code].word}!")
                return redirect(url_for("end", room_code=room_code))
        
    return render_template("index.html", values=active_room_codes[room_code].player_guesses[session["user"]], time=round(time.time() - active_room_codes[room_code].player_times[session["user"]], 3))


@app.route("/end/<room_code>", methods=["POST", "GET"])
def end(room_code):
    if request.method == "POST":
        # Race condition here
        if len(active_room_codes[room_code].completed) == len(active_room_codes[room_code].player_times) or \
            any([rnd > active_room_codes[room_code].round[session["user"]] for rnd in active_room_codes[room_code].round.values()]):
            return redirect(url_for("setup", room_code=room_code))
        else:
            flash("Wait for all players to finish playing")

    return render_template("end.html", word=active_room_codes[room_code].word, players=active_room_codes[room_code].completed.keys(), values=active_room_codes[room_code].completed)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)