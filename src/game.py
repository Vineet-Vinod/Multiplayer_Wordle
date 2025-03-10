from random import randint
from typing import List, Union

class Game: # Singleton Class
    __instance = None

    def __new__(cls, *args, **kwargs) -> "Game":
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def  __init__(self, file: str) -> None:
        """
        Initialize the Wordle Game instance by reading in the dictionary
        """
        with open(file, "r") as file:
            self.words = [line.strip() for line in file.readlines()]
            self.word_set = set(self.words)
        
    def generate_game_word(self) -> str:
        """
        Generate and return a random 5 letter word from the dictionary
        """
        return self.words[randint(0, len(self.words)-1)]

    def validate_guess(self, guess: str, orig: str) -> List[List[Union[str, int]]]:
        """
        Validates the player's guess against the original word

        Returns:
            A list of lists, where each inner list contains a character from the guessed word 
            and an integer code specifying its status
        """
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

    def run_guess(self, guess: str, orig: str) -> Union[List[List[Union[str, int]]], str]:
        """
        Checks the player guess before validating against the original word.
        
        Returns:
            str if the guess is not in the dictionary/is the original word
            List[List[Union[str, int]]] - the result of Game.validate_guess(...)
        """
        guess = guess.lower()
        if guess not in self.word_set: return "WND"
        if guess == orig: return "CS"
        else: return self.validate_guess(guess, orig)
