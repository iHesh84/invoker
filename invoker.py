import sqlite3
import random
import itertools


def sql():
    con = sqlite3.connect('invoker.db')
    con.execute('''CREATE TABLE IF NOT EXISTS scores (
        name TEXT,
        score INTEGER
        )
        ''')
    con.commit()
    con.close()


def main(con, name_input):
    # Dictionary of Invoker's spells, with the required orb combinations as keys
    # and the spell names as values
    spell_dict = {
        'Sun Strike': ['e', 'e', 'e'],
        'Cold Snap': ['q', 'q', 'q'],
        'Ghost Walk': ['q', 'q', 'w'],
        'Ice Wall': ['q', 'q', 'e'],
        'EMP': ['w', 'w', 'w'],
        'Tornado': ['w', 'w', 'q'],
        'Alacrity': ['w', 'w', 'e'],
        'Forge Spirit': ['e', 'e', 'q'],
        'Chaos Meteor': ['e', 'e', 'w'],
        'Deafening Blast': ['q', 'w', 'e']
    }
    # Initialize the score to 0
    score = 0
    while True:
        

        # Choose a random spell from the spell dictionary
        random_spell = random.choice(list(spell_dict.keys()))
        # Print the random spell
        print('\n', random_spell, '\n')

        # Prompt the player to enter a combination of orb abilities
        user_input = input('Enter: ').lower()
        found_spell = False

        # Iterate through the spells in the spell dictionary
        for spell in spell_dict.items():
            # Generate all possible combinations of the orb combination list
            combinations = [
                ''.join(combination) for combination in itertools.permutations(spell[1])]
            # Check the input string against each combination
            if user_input in combinations:
                # If a match is found, set the found_spell flag to True
                found_spell = True
                # If the player's input corresponds to the random spell, break out of the loop
                if spell[0] == random_spell:
                    score += 1
                    break
                # If the player's input does not correspond to the random spell, print "Incorrect" and quit the program
                else:
                    print("Incorrect")
                    break
            break

        # If the length of the player's input is not 3, print "Invalid input" and quit the program
        if len(user_input) != 3:
            print("Invalid input")
            break
        # If the input string is 3 characters long and no spell was found, print "Spell does not exist" and quit the program
        elif len(user_input) == 3 and not found_spell:
            print("Spell does not exist")
            break

    cursor = con.cursor()

    # Execute a SELECT query to retrieve all rows in the table with the same name
    cursor.execute("SELECT * FROM scores WHERE name=?", (name_input,))

    # Fetch the first row from the cursor
    row = cursor.fetchone()

    # If the row is not None, it means that the name already exists in the table
    if row is not None:
        # Update the score of the name in the table
        cursor.execute("UPDATE scores SET score=? WHERE name=?",
                        (score, name_input))
    else:
        # Insert a new record into the table with the name and score
        cursor.execute(
            "INSERT INTO scores (name, score) VALUES (?, ?)", (name_input, score))

    # Commit the transaction
    con.commit()

    # close the connection
    con.close()
    cursor.close()


if __name__ == '__main__':
    sql()
    main(sqlite3.connect('invoker.db'), input('Enter your name: '))
