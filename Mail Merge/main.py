PLACEHOLDER = '[name]'

with open("./Input/Names/invited_names.txt") as names_file:
    invited_names = [name.strip() for name in names_file.readlines()]

with open("Input/Letters/starting_letter.txt") as letter_file:
    letter_contents = letter_file.read()
    for name in invited_names:
        custom_letter = letter_contents.replace(PLACEHOLDER, name)
        with open(f"./Output/ReadyToSend/letter_for_{name}.txt", mode='w') as output_file:
            output_file.write(custom_letter)
