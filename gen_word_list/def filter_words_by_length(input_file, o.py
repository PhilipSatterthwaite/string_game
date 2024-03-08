def filter_words_by_length(input_file, output_file, min_length=4):
    with open(input_file, 'r') as f:
        words = [word.strip() for word in f.readlines() if len(word.strip()) >= min_length]

    with open(output_file, 'w') as f:
        f.write('\n'.join(words))

if __name__ == "__main__":
    input_file = "words_alpha.txt"  # Assuming words_alpha.txt is in the same directory
    output_file = "filtered_words.txt"
    
    filter_words_by_length(input_file, output_file)