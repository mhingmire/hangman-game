import tkinter as tk
from tkinter import messagebox, simpledialog
import random

#listing our 4 categories with all the words
#i just chose a few common words
categories_data = {
    "countries": [
        "canada", "brazil", "japan", "egypt", "australia",
        "france", "italy", "india", "china", "germany",
        "mexico", "spain", "russia", "south korea", "united kingdom",
        "united states", "argentina", "thailand", "south africa", "turkey",
        "bhutan", "kyrgyzstan", "malawi", "niger", "costa rica",
        "slovenia", "croatia", "estonia", "latvia", "lithuania",
        "panama", "bolivia", "uruguay", "paraguay", "moldova",
        "senegal", "morocco", "tunisia", "albania", "serbia"
    ],
    "f1": [
        "pitstop", "safety car", "drs", "formation lap", "lewis hamilton",
        "ferrari", "smooth operator", "carlos sainz", "charles leclerc",
        "lando norris", "yuki tsunoda", "george russell", "chassis",
        "max verstappen", "checo", "hammer time", "box"
    ],
    "disney movies": [
        "snow white and the seven dwarfs", "pinocchio", "fantasia", "dumbo",
        "bambi", "cinderella", "alice in wonderland", "peter pan",
        "sleeping beauty", "one hundred and one dalmatians", "the jungle book",
        "the little mermaid", "beauty and the beast", "aladdin", "the lion king",
        "mulan", "lilo & stitch", "tangled", "frozen", "shrek",
        "ratatouille", "kung fu panda", "madagascar", "cars",
        "inside out", "ice age"
    ],
    "desserts": [
        "tiramisu", "cheesecake", "brownie", "cupcake", "macaron", "donut",
        "churros", "baklava", "pavlova", "crepe", "gelato", "cannoli",
        "mochi", "ice cream", "panna cotta", "eclair", "apple pie",
        "key lime pie", "profiterole", "carrot cake", "chocolate mousse",
        "sticky toffee pudding", "flan", "rugelach", "sacher torte"
    ]
}

max_wrong = 6

hangman_pics = [
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
     o   |
         |
         |
         |
    =======""",
    """
     +---+
     |   |
     o   |
     |   |
         |
         |
    =======""",
    """
     +---+
     |   |
     o   |
    /|   |
         |
         |
    =======""",
    """
     +---+
     |   |
     o   |
    /|\\  |
         |
         |
    =======""",
    """
     +---+
     |   |
     o   |
    /|\\  |
    /    |
         |
    =======""",
    """
     +---+
     |   |
     o   |
    /|\\  |
    / \\  |
         |
    ======="""
]

hangman_colors = ["black", "red", "orange", "blue", "green", "purple", "maroon"]

#building the game logic
class hangman_game:
    def __init__(self):
        self.category = None
        self.reset_game()
        self.wins = 0
        self.losses = 0

    #shows all categories
    def choose_category(self):
        cats = list(categories_data.keys())
        self.category = random.choice(cats)  # default if user cancels
        return cats

    #setting the category as the category user chooses
    def set_category(self, category):
        self.category = category
        self.reset_game()

    
    def reset_game(self):
        if self.category:
            self.secret = random.choice(categories_data[self.category])
        else:
            self.secret = random.choice([w for cat in categories_data.values() for w in cat])
        self.correct = set()
        self.wrong = set()

    #this checks the letter entered and updates the game
    #basically updates the right or wong and won or lost
    def guess(self, letter):
        letter = letter.lower()
        if letter in self.correct or letter in self.wrong:
            return "already"
        if letter in self.secret:
            self.correct.add(letter)
            if self.is_won():
                self.wins += 1
                return "win"
            return "correct"
        else:
            self.wrong.add(letter)
            if self.is_lost():
                self.losses += 1
                return "lose"
            return "wrong"

    #this kind of is the main thing but not really at the same
    #this hides the original word to be guiessed as underscores;then reveals each letter if user guesses correctly
    def display_word(self):
        return " ".join([c if c in self.correct or not c.isalpha() else "_" for c in self.secret])

    #just returns the hangman picture at the stage the user is in
    def hangman_pic(self):
        return hangman_pics[len(self.wrong)]

    #changes the hangman colour based on the wrong guesses.
    def hangman_color(self):
        return hangman_colors[len(self.wrong)]

    #checks if you've guesssed all the letters correctly; if yes then you won
    def is_won(self):
        return set(c for c in self.secret if c.isalpha()) <= self.correct

    #checks the if you have reached the mazimum number of wrong guesses; if you did then you lost
    def is_lost(self):
        return len(self.wrong) >= max_wrong


#gui handles everything the user sees. i'm using tkinter
#it connects the game logic to buttons, labels and the hangman drawing.
class hangman_gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.game = hangman_game()

        #asking the category for user
        self.ask_category()

        #timer
        self.time_limit = 90  #90 seconds per round
        self.time_remaining = self.time_limit

        #timer label
        self.timer_label = tk.Label(root, text=f"Time left: {self.time_remaining}s", font=("helvetica", 12, "bold"))
        self.timer_label.pack(pady=5)

        #hangman picture
        self.hangman_label = tk.Label(root, text=self.game.hangman_pic(), font=("courier", 14), fg=self.game.hangman_color())
        self.hangman_label.pack(pady=10)

        #category label
        self.category_label = tk.Label(root, text=f"Category: {self.game.category}", font=("helvetica", 14, "italic"))
        self.category_label.pack(pady=5)

        #word display
        self.word_label = tk.Label(root, text=self.game.display_word(), font=("helvetica", 24))
        self.word_label.pack(pady=10)

        #wrong guesses display
        self.wrong_label = tk.Label(root, text="Wrong guesses: ", font=("helvetica", 12))
        self.wrong_label.pack(pady=5)

        #scoreboard
        self.score_label = tk.Label(root, text="Wins: 0 | Losses: 0", font=("helvetica", 12, "bold"))
        self.score_label.pack(pady=5)

        #letter buttons
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()
        self.letter_buttons = {}
        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
            b = tk.Button(self.buttons_frame, text=letter.upper(), width=4, command=lambda l=letter: self.click_letter(l))
            b.grid(row=i//9, column=i%9, padx=2, pady=2)
            self.letter_buttons[letter] = b

        #reset button
        self.reset_button = tk.Button(root, text="Play Again", command=self.reset)
        self.reset_button.pack(pady=10)

        #keyboard support
        root.bind("<Key>", self.key_pressed)

        #starting the timeer
        self.start_timer()

    #asking the user to choose category
    def ask_category(self):
        cats = self.game.choose_category()
        category = simpledialog.askstring("Choose Category", f"Pick a category from the following:\n{', '.join(cats)}")
        if category:
            cat_lower = category.strip().lower()
            matched = next((c for c in cats if c.lower() == cat_lower), None)
            if matched:
                self.game.set_category(matched)
                return
        messagebox.showinfo("hangman", f"No valid category chosen. Defaulting to {self.game.category}")
        self.game.set_category(self.game.category)

    #starting or resetting timeer
    def start_timer(self):
        self.time_remaining = self.time_limit
        self.update_timer()

    # updating the timer every second
    def update_timer(self):
        self.timer_label.config(text=f"Time Left: {self.time_remaining}s")
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            messagebox.showinfo("hangman", f"⏰ Time's up! the word was '{self.game.secret}'")
            self.game.losses += 1
            self.update_display()
            self.disable_letters()

    #so this helps to write with keyboard keys too rather than clicking the keyboard on the screen
    def key_pressed(self, event):
        letter = event.char.lower()
        if letter.isalpha() and letter in self.letter_buttons and self.letter_buttons[letter]['state'] == 'normal':
            self.click_letter(letter)

    # handling button clicks
    def click_letter(self, letter):
        result = self.game.guess(letter)
        self.update_display()
        self.letter_buttons[letter].config(state="disabled")
        if result == "already":
            messagebox.showinfo("hangman", f"You already guessed '{letter}'")
        elif result == "win":
            messagebox.showinfo("hangman", f"🎉 You won! the word was '{self.game.secret}'")
            self.disable_letters()
        elif result == "lose":
            messagebox.showinfo("hangman", f"💀 You lost! the word was '{self.game.secret}'")
            self.disable_letters()

    #updating all tje labels
    def update_display(self):
        self.hangman_label.config(text=self.game.hangman_pic(), fg=self.game.hangman_color())
        self.word_label.config(text=self.game.display_word())
        self.wrong_label.config(text=f"Wrong Guesses: {' '.join(sorted(self.game.wrong))}")
        self.score_label.config(text=f"Wins: {self.game.wins} | Losses: {self.game.losses}")
        self.category_label.config(text=f"Category: {self.game.category}")


    def disable_letters(self):
        for b in self.letter_buttons.values():
            b.config(state="disabled")

    # eset game and timer
    def reset(self):
        self.ask_category()
        self.game.reset_game()
        self.update_display()
        for b in self.letter_buttons.values():
            b.config(state="normal")
        self.start_timer()

#finally running the whole game
if __name__ == "__main__":
    root = tk.Tk()
    gui = hangman_gui(root)
    root.mainloop()
