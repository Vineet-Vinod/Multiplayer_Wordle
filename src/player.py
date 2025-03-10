class Player:
    def __init__(self, player_name, player_id):
        self.keyboard = None
        self.guesses = []
        self.time = 0
        self.prev = 0
        self.completed = False
        self.done = False
        self.name = player_name
        self.sid = player_id
    
    def reset(self):
        self.keyboard = [[['Q', 0], ['W', 0], ['E', 0], ['R', 0], ['T', 0], ['Y', 0], ['U', 0], ['I', 0], ['O', 0], ['P', 0]],
                         [['A', 0], ['S', 0], ['D', 0], ['F', 0], ['G', 0], ['H', 0], ['J', 0], ['K', 0], ['L', 0]],
                         [['Z', 0], ['X', 0], ['C', 0], ['V', 0], ['B', 0], ['N', 0], ['M', 0]]]
        self.guesses.clear()
        self.time = 0
        self.completed = False
        self.done = False

    def update_after_guess(self, result, time):
        if result == "CS":
            self.done = True
            self.completed = True
            self.guesses.append("CS")

        elif result == "WND":
            self.guesses.append("WND")
            
        else:
            for c, col in result:
                if (idx := "QWERTYUIOP".find(c)) != -1:
                    self.keyboard[0][idx][1] = col
                elif (idx := "ASDFGHJKL".find(c)) != -1:
                    self.keyboard[1][idx][1] = col
                else:
                    self.keyboard[2]["ZXCVBNM".find(c)][1] = col
            
            self.guesses.append(result)
            if len(self.guesses) == 6:
                self.done = True

        self.time = float(time)

        return self.done
    