import tkinter as tk
from tkinter import messagebox
import random
import links  # Assuming you have a module named links that contains the find_links function

def get_user_string(entry, answer, letters, guessed_list):
    guess = entry.get().upper()
    entry.delete(0, tk.END)  # Clear the entry field after getting the input
    

    if guess == answer:
        messagebox.showinfo("Result", "Correct!")
    if all(char in letters for char in guess): # check valid letters
        if len(guess) >= 3:                    # check long enough
            if guess not in guessed_list:      # check if in list
                return guess
            else:
                messagebox.showinfo("Word already guessed. Try another one.")
        else:
            messagebox.showinfo("Too short.")
    else:
        messagebox.showinfo("Bad letters.")

def create_gui(answer):
    root = tk.Tk()
    root.title("PANGRAMS")

    # Generate scrambled letters
    unique_letters = ''.join(set(answer))
    scrambled_letters = ''.join(random.sample(unique_letters, len(unique_letters)))

    # Display scrambled letters
    scrambled_label = tk.Label(root, text="Scrambled Letters: " + scrambled_letters)
    scrambled_label.pack()

    # Entry field for user guesses
    entry = tk.Entry(root)
    entry.pack()
    guessed_list = []  # List to store guessed words
    # Button to submit guesses
    submit_button = tk.Button(root, text="Submit", command=lambda: get_user_string(entry, answer, unique_letters, guessed_list))
    
    submit_button.pack()

    root.mainloop()