import wordfreq
import spacy

def filter_words_by_length(input_file, output_file, min_length=4):
    with open(input_file, 'r') as f:
        # Filter words based on length and absence of 'S'
        words = [word.strip() for word in f.readlines() if len(word.strip()) >= min_length and (word.strip()[-1] != 'S' or word.strip()[-2] == 'S')]
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(words))

def find_pangrams(input_file, output_file, length):
    with open(input_file, 'r') as f:
        words = [word.strip() for word in f.readlines()]
    pangrams = [word for word in words if len(set(word)) == length]

    with open(output_file, 'w') as f:
        f.write("\n".join(pangrams))

def find_perfect(input_file, output_file, length):
    with open(input_file, 'r') as f:
        perfect_words = [word.strip() for word in f if len(word.strip()) == length]

    with open(output_file, 'w') as f:
        f.write('\n'.join(perfect_words))


def is_proper_noun(token):
    return token.pos_ == 'PROPN'  # Check if token is a proper noun

def find_real(input_file, output_file, freq):
    # Load spaCy's English language model
    nlp = spacy.load('en_core_web_sm')

    # Create a set to store unique words
    words_set = set()

    # Open input file and collect unique words
    with open(input_file, 'r') as f:
        # Process the entire file content as a single text
        text = f.read()

    # Tokenize the text using spaCy
    doc = nlp(text)

    # Check each token in the document
    for token in doc:
        # Check if the token is a proper noun and frequency is above threshold
        if not is_proper_noun(token) and wordfreq.word_frequency(token.text, 'en', wordlist='best', minimum=0.0) > freq:
            words_set.add(token.text)

    # Write unique words to the output file
    with open(output_file, 'w') as f:
        for word in words_set:
            f.write(f"{word}\n")
        
        

# Inputs --------------------------------------------------
filter_length_bool = True
find_pangrams_bool = True
pangram_length = 7
find_perfect_bool = True
filter_infreq_bool = True
frequency = 10 ** (-6) #between 0 and 1


# --------------------------------------------------------
#1. filter out words less than 4 letters long. get rid of S plurals (ending in SS is ok)
#2. find pangrams with the correct number of letters
#3. find perfect pangrams
#4. filter pangrams

if __name__ == "__main__":
    if filter_length_bool is True:
        input_file = "z_words_alpha.txt"
        output_file = "z_filtered_words.txt"
        filter_words_by_length(input_file, output_file)

    if find_pangrams_bool is True:
        input_file = "z_filtered_words.txt"
        output_file = f"z_pangrams_{pangram_length}.txt"
        find_pangrams(input_file, output_file, pangram_length)
    
    if find_perfect_bool is True:
        input_file = f"z_pangrams_{pangram_length}.txt"
        output_file = f"z_perfect_{pangram_length}.txt"
        find_perfect(input_file, output_file, pangram_length)

    if filter_infreq_bool == True:
        input_file = f"z_perfect_{pangram_length}.txt"
        output_file = f"z_perfectfilt_{pangram_length}.txt"
        find_real(input_file, output_file, frequency)