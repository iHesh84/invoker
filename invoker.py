import sqlite3
import random
import itertools

def create_table():
    con = sqlite3.connect('invoker.db')

    con.execute('''CREATE TABLE IF NOT EXISTS scores (
        name TEXT,
        high_score INTEGER
        )
        ''')

    con.commit()
    con.close()
    
def update_high_score(name, high_score):
    try:
        con = sqlite3.connect('invoker.db')

        cursor = con.cursor()

        cursor.execute("SELECT * FROM scores WHERE name=?", (name,))

        row = cursor.fetchone()

        if row is not None:
            if high_score > row[1]:
                cursor.execute("UPDATE scores SET high_score=? WHERE name=?", (high_score, name))
        else:
            cursor.execute("INSERT INTO scores (name, high_score) VALUES (?, ?)", (name, high_score))
        
        # Commit the update to the database
        con.commit()

    except sqlite3.Error as e:
        print(e)

    

def main():
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
    high_score = 0
    game_ended = False
    while game_ended == False:
        

        random_spell = random.choice(list(spell_dict.keys()))
        print('\n', random_spell, '\n')

        user_input = input('Enter: ').lower()
        found_spell = False

        for spell in spell_dict.items():
            combinations = [
                ''.join(combination) for combination in itertools.permutations(spell[1])]
            if user_input in combinations:
                found_spell = True
                if spell[0] == random_spell:
                    high_score += 1
                    break
                else:
                    print("Incorrect")
                    game_ended = True
                    break

            

        if len(user_input) != 3:
            print("Invalid input")
            break
        elif len(user_input) == 3 and not found_spell:
            print("Spell does not exist")
            break
    
    print("You scored:", high_score)
    update_high_score(name_input, high_score)


if __name__ == '__main__':
    name_input = input('Enter your name: ')
    create_table()
    main()
