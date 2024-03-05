import random
import links
import game_GUI as gui


def get_user_string(letters, guessed_list):
    while True:
        user_input = input("Enter a guess: ").upper()
        
        if all(char in letters for char in user_input): # check valid letters
            if len(user_input) >= 3:                    # check long enough
                if user_input not in guessed_list:      # check if in list
                    return user_input
                else:
                    print("Word already guessed. Try another one.")
            else:
                print("Too short.")
        else:
            print("Bad letters.")


if __name__ == "__main__":
    answer = "AUGMENT"
    guessed_list = []
    unique_letters = ''.join(set(answer))

    #gui.create_gui(answer)
    #letters = set(answer)
    #guess = gui.get_user_string(letters, answer, guessed_list)
    #word_colors = links.find_links(guess, answer)
    #print(word_colors)  # For testing purposes, you can print the word colors to the console
    scrambled_letters = ''.join(random.sample(unique_letters, len(unique_letters)))
    print(scrambled_letters)
    guessed_list = []
    guess = ""
    while guess != answer:
        guess = get_user_string(scrambled_letters, guessed_list)
        guessed_list.append(guess)
        if guess == answer:
            break
        else:
            word_colors = links.find_links(guess, answer)
            print(word_colors)
    




