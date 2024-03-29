from flask import Flask, render_template, request
import random
import links
import math
from gen_word_list.gen_word_list import make_word_list

app = Flask(__name__)
app.static_folder = 'static'
answer = "FRAILTY"
unique_letters = ''.join(set(answer))
scrambled_letters = ''.join(random.sample(unique_letters, len(unique_letters)))
guessed_list = []
colors_list = []
guess = ""
correct_guess = False
allowed_words = make_word_list(answer)
link_locs = []

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
    global link_locs
    guess = ""
    guessed_list = []
    colors_list = []
    correct_guess = False
    link_locs = []

def get_user_string(letters, guessed_list, allowed_words):
    user_input = request.form['guess'].upper()
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
    global link_locs

    if request.method == 'POST':
        guess, error_message = get_user_string(scrambled_letters, guessed_list, allowed_words)
        if error_message is not None:
            return render_template(
                'index.html', 
                scrambled_letters=scrambled_letters, 
                error_message=error_message, 
                guessed_list=guessed_list, 
                colors_list=colors_list, 
                correct_guess=correct_guess,
                link_locs = link_locs)
        guessed_list.append(guess)
        if guess == answer:
            correct_guess = True
        
        word_colors, G_locs = links.find_links(guess, answer)
        link_locs.append(G_locs)
        colors_list.append(word_colors)
    elif request.method == 'GET':
        form_data   = dict(request.form)  # Convert ImmutableMultiDict to dict
        if 'action' not in form_data:
            form_data['action'] = ['new_word']
        if form_data['action'][0] == 'new_word':
            reset_variables()
            scrambled_letters = ''.join(random.sample(unique_letters, len(unique_letters)))
    return render_template(
        'index.html',
        scrambled_letters=scrambled_letters,
        guessed_list=guessed_list,
        colors_list=colors_list,
        correct_guess=correct_guess,
        link_locs = link_locs
    )
if __name__ == '__main__':

    app.run(debug=True)
