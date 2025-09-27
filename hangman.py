#!/usr/bin/env python3
"""
Terminal Hangman game (Python).
Run: python hangman.py
"""

import random
import sys

WORDS = [
    "computer", "hangman", "python", "university", "algorithm", "datastructure",
    "programming", "network", "database", "compiler"
]

HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =======""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =======""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    ======="""
]

MAX_WRONG = len(HANGMAN_PICS) - 1

def choose_word():
    return random.choice(WORDS).lower()

def display_state(secret, correct_guesses, wrong_guesses):
    print(HANGMAN_PICS[len(wrong_guesses)])
    shown = " ".join([c if c in correct_guesses else "_" for c in secret])
    print("\nWord: ", shown)
    print("Wrong guesses:", " ".join(sorted(wrong_guesses)))
    print(f"Attempts left: {MAX_WRONG - len(wrong_guesses)}\n")

def get_guess(already_guessed):
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).")
            continue
        if guess in already_guessed:
            print("You've already guessed that letter. Try another.")
            continue
        return guess

def play_round():
    secret = choose_word()
    correct = set()
    wrong = set()

    while True:
        display_state(secret, correct, wrong)
        if set(secret) <= correct:
            print("🎉 You guessed it! The word was:", secret)
            return True
        if len(wrong) >= MAX_WRONG:
            print(HANGMAN_PICS[-1])
            print("💀 You lost. The word was:", secret)
            return False
        guess = get_guess(correct | wrong)
        if guess in secret:
            print("Nice! That letter is in the word.")
            correct.add(guess)
        else:
            print("Nope. That letter is not in the word.")
            wrong.add(guess)

def main():
    print("Welcome to Hangman!\n")
    random.seed()
    while True:
        play_round()
        again = input("\nPlay again? (Yes/No): ").strip().lower()
        if not again or again[0] != "y":
            print("Thanks for playing — bye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
