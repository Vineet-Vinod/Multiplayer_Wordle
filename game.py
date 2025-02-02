from random import randint
from collections import defaultdict


class Room: # Room struct
    def __init__(self):
        self.word = None
        self.player_guesses = defaultdict(list)
        self.player_times = {}
        self.completed = {}
        self.players = 1
        self.round = defaultdict(int)

class Game:
    WORD_LEN = 5
    words = []
    word_set = set()


    def  __init__(self, file):
        if not len(Game.words):
            with open(file, "r") as file:
                Game.words = [line.strip() for line in file.readlines()]
                Game.word_set = set(self.words)
        

    def generate_game_word(self):
        return Game.words[randint(0, len(self.words)-1)]


    def validate_guess(self, guess, orig):
        ret = ['B'] * Game.WORD_LEN # Wrong letter (default)
        not_g = []
        not_w = []

        for i, c in enumerate(guess):
            if c == orig[i]:
                ret[i] = 'G' # Correct letter, right spot
            else:
                not_g.append((c, i))
                not_w.append(orig[i])
        
        for c, i in not_g:
            if c in not_w:
                ret[i] = 'Y' # Correct letter, wrong spot
                not_w.remove(c)
        
        return ret
    

    def run_guess(self, guess, orig):
        if guess not in self.word_set: return "Word not in dictionary"
    
        if guess == orig: return "Correct, you solved it!"
        else: return f"{guess}: {"".join(self.validate_guess(guess, orig))}"
