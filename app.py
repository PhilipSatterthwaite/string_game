from flask import Flask, render_template, request, session
import random
import math
from string_game.gen_word_list import gen_word_list
from string_game import links

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def pick_random_word(file_path):
    with open(file_path, 'r') as f:
        words = f.readlines()
        random_word = random.choice(words).strip().upper()  # Remove leading/trailing whitespace
    return random_word

#-------------------------------------------------------------------------------------
answer = "WORKING" #pick_random_word("/home/noclue/string_game/gen_word_list/z_perfectfilt_7.txt")
gen_file = True
#-------------------------------------------------------------------------------------

unique_letters = ''.join(set(answer))
scrambled_letters = ''.join(random.sample(unique_letters, len(unique_letters)))



if gen_file == True:
    allowed_words = gen_word_list.make_word_list(answer)
else:
    allowed_words = []
    # Open the file in read mode
    with open('/home/noclue/string_game/valid_words.txt', 'r') as file:
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
    session['guessed_list'] = []
    session['colors_list'] = []
    session['guess'] = ""
    session['correct_guess'] = False
    session['link_locs'] = []

def get_user_string(letters, guessed_list, allowed_words):
    user_input = request.form['guess'].upper()
    if all(char in letters for char in user_input): # check valid letters
        if len(user_input) >= 3:                    # check long enough
            if user_input not in guessed_list:      # check if in list
                if user_input in allowed_words:     #check if word
                    return user_input, None  
                return user_input, "Not a word."
            else:
                return user_input, "Already guessed."
        else:
            return user_input, "Too short."
    else:
        return user_input, "Bad letters."

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'guessed_list' not in session:
        reset_variables()

    if request.method == 'POST':
        guess, error_message = get_user_string(session['scrambled_letters'], session['guessed_list'], allowed_words)
        if error_message:
            return render_template(
                'index.html',
                scrambled_letters=session['scrambled_letters'],
                error_message=error_message,
                guessed_list=session['guessed_list'],
                colors_list=session['colors_list'],
                correct_guess=session['correct_guess'],
                link_locs=session['link_locs']
            )
        guessed_list_update = session.get('guessed_list', []).copy()
        guessed_list_update.append(guess)
        session['guessed_list'] = guessed_list_update   
        if guess == answer:
            session['correct_guess'] = True

        word_colors, G_locs = links.find_links(guess, answer)
        session['link_locs'].append(G_locs)
        session['colors_list'].append(word_colors)
    elif request.method == 'GET':
        form_data = dict(request.form)  # Convert ImmutableMultiDict to dict
        if 'action' not in form_data:
            form_data['action'] = ['new_word']
        if form_data['action'][0] == 'new_word':
            reset_variables()
            session['scrambled_letters'] = ''.join(random.sample(unique_letters, len(unique_letters)))

    return render_template(
        'index.html',
        scrambled_letters=session['scrambled_letters'],
        guessed_list=session['guessed_list'],
        colors_list=session['colors_list'],
        correct_guess=session['correct_guess'],
        link_locs=session['link_locs']
    )

if __name__ == '__main__':

    app.run(debug=True)
