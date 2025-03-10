from random import randint

class Game: # Singleton class
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls) # Create an object of type cls
        return cls.__instance

    def  __init__(self, file):
        with open(file, "r") as file:
            self.words = [line.strip() for line in file.readlines()]
            self.word_set = set(self.words)
        
    def generate_game_word(self):
        return self.words[randint(0, len(self.words)-1)]

    def validate_guess(self, guess, orig):
        ret = [[chr(ord(c)-32), 3] for c in guess] # Wrong letter (default)
        not_g = []
        not_w = []

        for i, c in enumerate(guess):
            if c == orig[i]:
                ret[i][1] = 2 # Correct letter, right spot
            else:
                not_g.append((c, i))
                not_w.append(orig[i])
        
        for c, i in not_g:
            if c in not_w:
                ret[i][1] = 1 # Correct letter, wrong spot
                not_w.remove(c)
        
        return ret

    def run_guess(self, guess: str, orig):
        guess = guess.lower()
        if guess not in self.word_set: return "WND"
        if guess == orig: return "CS"
        else: return self.validate_guess(guess, orig)
