import pandas as pd
alphabet = pd.read_csv('data/nato_phonetic_alphabet.csv')

#Loop through rows of a data frame
alphabet_dict = {row.letter:row.code for index, row in alphabet.iterrows()}

# result = [alphabet_dict[letter] for letter in word if letter in alphabet_dict]

def generate_phonetic():
    word = input('Enter a word: ').upper()
    try:
        result = [alphabet_dict[letter] for letter in word]
    except KeyError:
        print("Sorry, only letters in the alphabet please")
        generate_phonetic()
    else:
        print(result)

generate_phonetic()
