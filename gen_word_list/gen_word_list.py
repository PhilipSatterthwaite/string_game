
def make_word_list(word):

    input_file = "/home/noclue/string_game/gen_word_list/z_words_alpha.txt"  # Assuming words_alpha.txt is in the same directory
    output_file = "/home/noclue/string_game/valid_words.txt"
    letter_set = ''.join(sorted(set(word.lower()), key=word.lower().index))  # Obtain unique letters while preserving order

    with open(input_file, 'r') as f:
        
        lines = f.readlines()
        cleaned_lines = [line.strip().lower() for line in lines]
        words = [word.upper() for word in cleaned_lines if set(word).issubset(set(letter_set))]
        


    with open(output_file, 'w') as f:
        f.write('\n'.join(words))
    return words
