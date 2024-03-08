from flask import Flask, render_template, request
import random
import links
import math

app = Flask(__name__)
answer = "FRAILTY"
unique_letters = ''.join(set(answer))
scrambled_letters = ''.join(random.sample(unique_letters, len(unique_letters)))
guessed_list = []
colors_list = []
guess = ""
correct_guess = False
allowed_words = []
# Open the file in read mode
with open('filtered_words.txt', 'r') as file:
    for line in file:
        allowed_words.append(line.strip())

def calculate_cos(angle):
    return math.cos(angle)

def calculate_sin(angle):
    return math.sin(angle)


# Add the custom functions to the Jinja2 environment
app.jinja_env.globals.update(calculate_cos=calculate_cos)
app.jinja_env.globals.update(calculate_sin=calculate_sin)

def reset_variables():
    global guessed_list
    global colors_list
    global guess
    global correct_guess
    guess = ""
    guessed_list = []
    colors_list = []
    correct_guess = False

def get_user_string(letters, guessed_list, allowed_words):
    user_input = request.form['guess'].upper()
    print(user_input)
    print(request.form)
    if all(char in letters for char in user_input): # check valid letters
        if len(user_input) >= 3:                    # check long enough
            if user_input not in guessed_list:      # check if in list
                if user_input not in allowed_words:
                    return user_input, "Not a word."
                return user_input, None
            else:
                return user_input, "Already guessed."
        else:
            return user_input, "Too short."
    else:
        return user_input, "Bad letters."

@app.route('/', methods=['GET', 'POST'])
def index():
    global guessed_list
    global guess
    global scrambled_letters
    global colors_list
    global correct_guess
    global allowed_words

    if request.method == 'POST':
        guess, error_message = get_user_string(scrambled_letters, guessed_list, allowed_words)
        if error_message is not None:
            return render_template('index.html', scrambled_letters=scrambled_letters, error_message=error_message, guessed_list=guessed_list, colors_list=colors_list, correct_guess=correct_guess)
        guessed_list.append(guess)
        if guess == answer:
            green_string = 'G' * len(answer)
            colors_list.append(green_string)
            correct_guess = True
            return render_template('index.html', scrambled_letters=scrambled_letters, guessed_list=guessed_list, colors_list=colors_list, correct_guess=correct_guess)
        else:
            word_colors = links.find_links(guess, answer)
            colors_list.append(word_colors)
    elif request.method == 'GET':
        form_data   = dict(request.form)  # Convert ImmutableMultiDict to dict
        if 'action' not in form_data:
            form_data['action'] = ['new_word']
        if form_data['action'][0] == 'new_word':
            reset_variables()
            scrambled_letters = ''.join(random.sample(unique_letters, len(unique_letters)))
    return render_template('index.html', scrambled_letters=scrambled_letters, guessed_list=guessed_list, colors_list=colors_list, correct_guess=correct_guess)

if __name__ == '__main__':

    app.run(debug=True)
