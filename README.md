# Multiplayer Wordle  

In this project, we will build a multiplayer version of Wordle.  

## Tech Stack  
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask, Flask-SocketIO)  

## Features  
- Real-time multiplayer support using WebSockets  
- Basic frontend design principles  
- Backend API design for handling game logic  

## 📺 YouTube Playlist  
Watch the full tutorial series here: [Multiplayer Wordle - YouTube](https://youtube.com/playlist?list=PLzC38h82FLMs5d5jdfchww37PFcT7GBKB)  

---

## 🚀 How to Run  

### 1️⃣ Clone the Repository  
```sh
git clone https://github.com/Vineet-Vinod/Multiplayer_Wordle.git
cd Multiplayer_Wordle
```

### 2️⃣ Set Up a Virtual Environment, Install Dependencies and Run 
#### 🔹 Windows  
```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### 🔹 Linux/MacOS  
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

### 3️⃣ Access the Game  
Open your browser and go to:  
🔗 **http://localhost:5000**  

If you want to play with others on the same network (it is multiplayer after all), share your **subnet IP address** (found using `ipconfig` on Windows or `ifconfig` on Linux/Mac) at port **5000**.  

The host is set to `0.0.0.0` in `app.py`, allowing it to accept connections from your local network.  
