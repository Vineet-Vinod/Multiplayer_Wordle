// div visibility functions
function turn_off_login() { document.querySelector(".login").style.display = "none"; };
function turn_on_login() { document.querySelector(".login").style.display = "block"; };

function turn_off_lobby() { document.querySelector(".lobby").style.display = "none"; };
function turn_on_lobby() { document.querySelector(".lobby").style.display = "block"; };

function turn_off_room() { document.querySelector(".room").style.display = "none"; };
function turn_on_room() { document.querySelector(".room").style.display = "block"; };

function turn_off_game() { document.querySelector(".game").style.display = "none"; };
function turn_on_game() { document.querySelector(".game").style.display = "block"; };

function turn_off_end() { document.querySelector(".end").style.display = "none"; };
function turn_on_end() { document.querySelector(".end").style.display = "block"; };


// Standard message function
function showMessage(message, duration = 3000) {
    let messageDiv = document.createElement("div");
    messageDiv.textContent = message;
    messageDiv.style.position = "fixed";
    messageDiv.style.top = "10px";
    messageDiv.style.left = "50%";
    messageDiv.style.transform = "translateX(-50%)";
    messageDiv.style.background = "rgba(0, 123, 255, 0.9)";
    messageDiv.style.color = "white";
    messageDiv.style.padding = "10px 20px";
    messageDiv.style.borderRadius = "5px";
    messageDiv.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.remove();
    }, duration);
}


// Initial page load
turn_off_lobby();
turn_off_room();
turn_off_game();
turn_off_end();
let socket = io();


// Page Functions
function login_user() {
    let username = document.getElementById("login_text").value;
    socket.emit("login_user", { "username": username });
}

function new_room() {
    let username = document.getElementById("username").textContent;
    socket.emit("new_room");
}

function join_room() {
    let username = document.getElementById("username").textContent;
    let room_code = document.getElementById("lobby_join_code").value;
    socket.emit("join_room", { "room_code": room_code });
}

function start_game() {
    let username = document.getElementById("username").textContent;
    let room_code = document.getElementById("room_code").textContent;
    socket.emit("start_game", { "username": username, "room_code": room_code });
}

function guess_word() {
    let username = document.getElementById("username").textContent;
    let room_code = document.getElementById("room_code").textContent;
    let guess = document.getElementById("game_guess").value;
    document.getElementById("game_guess").value = "";
    socket.emit("game_guess", { "username": username, "room_code": room_code, "game_guess": guess, "time": curr_time });
}

let colors_array = ["grey", "orange", "green", "black"];
function print_guesses(list_of_guesses) {
    let game_guesses = document.getElementById("game_guesses");
    game_guesses.innerHTML = "";

    for (let i = 0; i < list_of_guesses.length; i++) {
        let line = document.createElement("p");

        for (let j = 0; j < list_of_guesses[i].length; j++) {
            let letter = document.createElement("span");
            letter.style.color = colors_array[list_of_guesses[i][j][1]];
            letter.style.fontSize = "24px";
            letter.textContent = list_of_guesses[i][j][0];
            line.appendChild(letter);
        }

        game_guesses.appendChild(line);
    }
}

function print_keyboard(keyboard) {
    let game_keyboard = document.getElementById("game_keyboard");
    game_keyboard.innerHTML = "";

    for (let i = 0; i < keyboard.length; i++) {
        let line = document.createElement("p");

        for (let j = 0; j < keyboard[i].length; j++) {
            let letter = document.createElement("span");
            letter.style.color = colors_array[keyboard[i][j][1]];
            letter.style.fontSize = "36px";
            letter.style.padding = "10px";
            letter.textContent = keyboard[i][j][0];
            line.appendChild(letter);
        }

        game_keyboard.appendChild(line);
    }
}

function print_leaderboard(leaderboard) {
    let end_leaderboard = document.getElementById("end_leaderboard");
    end_leaderboard.innerHTML = "";

    for (let i = 0; i < leaderboard.length; i++) {
        let line = document.createElement("p");
        line.textContent = `${leaderboard[i][0]} - Completed: ${leaderboard[i][1]}   Guesses: ${leaderboard[i][2]}   Time: ${Math.floor(leaderboard[i][3] / 10)}.${leaderboard[i][3] % 10} seconds`;
        end_leaderboard.appendChild(line);
    }
}


// Event listeners for buttons
document.getElementById("login_button").addEventListener("click", login_user);
document.getElementById("lobby_new").addEventListener("click", new_room);
document.getElementById("lobby_join").addEventListener("click", join_room);
document.getElementById("room_start_game").addEventListener("click", start_game);
document.getElementById("game_submit").addEventListener("click", guess_word);
document.getElementById("end_start_game").addEventListener("click", start_game);


// Stopwatch
let stopwatch_ref = undefined;
let curr_time = 0;
function Stopwatch() {
    curr_time = 0;
    stopwatch_ref = setInterval(() => {
        document.getElementById("game_time").textContent = `${Math.floor(curr_time / 10)}.${curr_time%10} seconds`;
        curr_time++;
    }, 100);
}


// Socket communications
socket.on("login_valid_username", (login_json) => {
    turn_off_login();
    turn_on_lobby();
    document.getElementById("username").textContent = login_json.username;
    document.getElementById("username").style.display = "block";
});

socket.on("invalid", (error_json) => {
    showMessage(error_json.error);
});

socket.on("room_valid", (room_json) => {
    turn_off_lobby();
    turn_off_end();
    turn_on_room();
    document.getElementById("room_code").textContent = room_json.room_code;
    document.getElementById("room_code").style.display = "block";
    document.getElementById("room_players").textContent = "There are " + room_json.room_players + " players in the room";
});

socket.on("game_load", (game_json) => {
    turn_off_room();
    turn_off_end();
    turn_on_game();
    
    document.getElementById("end_leaderboard").innerHTML = "";
    document.getElementById("game_keyboard").innerHTML = "";
    document.getElementById("game_guesses").innerHTML = "";

    Stopwatch();
    print_keyboard(game_json.keyboard);
});

socket.on("game_valid_guess", (game_json) => {
    print_guesses(game_json.guesses);
    print_keyboard(game_json.keyboard);
});

socket.on("end_page", (end_json) => {
    clearInterval(stopwatch_ref);
    stopwatch_ref = undefined;
    turn_off_game();
    turn_on_end();
    document.getElementById("end_word").textContent = "The correct word was " + end_json.correct_word;
    print_leaderboard(end_json.leaderboard);
});
