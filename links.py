

def gen_strings(word: str, is_ans):
    
    if is_ans is True:
        raw = [word[i:i+n] for n in range(2, len(word)+1) for i in range(len(word)-n+1)]
        reduced = list(set(raw))
        return reduced
    else:
        raw = [word[i:i+n] for n in range(2, len(word)+1) for i in range(len(word)-n+1)]
        return raw

def find_links(guess, answer):
    guess_links = gen_strings(guess, False)
    answer_links = gen_strings(answer, True)
    correct_links = list(set(guess_links) & set(answer_links))
    colored = ['X'] * len(guess)
    
    G_locs = []
    for link in correct_links:
        locations = [i for i in range(len(guess)) if guess.startswith(link, i)]  # Find all occurrences of the link in guess
        for location in locations:
            G_locs.append([location, len(link)])

    # Sort G_locs based on the first subelement of each element in ascending order
    G_locs.sort(key=lambda x: x[0])

    # Initialize a dictionary to keep track of the maximum second subelement for each unique first subelement
    max_lengths = {}
    for location, length in G_locs:
        if location not in max_lengths or length > max_lengths[location]:
            max_lengths[location] = length
    
    # Filter G_locs to keep only the elements with the largest second subelement for each unique first subelement
    G_locs = [[location, length] for location, length in G_locs if length == max_lengths[location]]
    # Loop through each element A
    for idx_a, element_a in enumerate(G_locs):
        a_sum = sum(element_a)
        # Compare element A with all other elements B
        for idx_b, element_b in enumerate(G_locs):
            b_sum = sum(element_b)
            if idx_b > idx_a and b_sum <= a_sum:
                G_locs[idx_b] = [-1,-1] # Delete element B if its sum is less than or equal to A's sum

    G_locs = [element for element in G_locs if element != [-1, -1]]
    G_locs_saved = G_locs.copy()

    if not G_locs:
        return ''.join(colored), G_locs
    while True:
        col_tag = 'G'
        
        loc = G_locs[0]
        for i in range(loc[0], loc[0] + loc[1]):
            colored[i] = col_tag
        if len(G_locs) == 1:
            break
        else:
            del G_locs[0]
    
    if sorted(set(guess)) == sorted(set(answer)) and guess != answer:
        return ''.join(colored).lower(), G_locs_saved

    return ''.join(colored), G_locs_saved

word = find_links('BITTERNUT', 'TRIBUTE')
print(word)
