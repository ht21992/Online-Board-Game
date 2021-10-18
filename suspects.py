import random
import pickle

with open("run_number", 'rb') as f:
    run_number = pickle.load(f)




def sus_info():
    global run_number
    suspects = {0: {"Name": "John L Huff", "Blood Type": "AB+", "Occupation": "actor", "Hair Color": "brown", "Age": 64,
                    "Sex": "man"},
                1: {"Name": "Eric B Chatfield", "Blood Type": "A+", "Occupation": "painter", "Hair Color": "black",
                    "Age": 32, "Sex": "man"},
                2: {"Name": "Elizabeth Demby", "Blood Type": "B+", "Occupation": "surgeon", "Hair Color": "black",
                    "Age": 28, "Sex": "woman"},
                3: {"Name": "Christina Trujillo", "Blood Type": "A+", "Occupation": "tailor", "Hair Color": "blonde",
                    "Age": 41, "Sex": "woman"},
                4: {"Name": "David Devries", "Blood Type": "O+", "Occupation": "surgeon", "Hair Color": "blonde",
                    "Age": 29, "Sex": "man"},
                5: {"Name": "Kathleen Keller", "Blood Type": "AB+", "Occupation": "nurse", "Hair Color": "brown",
                    "Age": 52, "Sex": "woman"},
                6: {"Name": "Norma Shields", "Blood Type": "O+", "Occupation": "painter", "Hair Color": "black",
                    "Age": 27, "Sex": "woman"},
                7: {"Name": "Stephanie Cook", "Blood Type": "O-", "Occupation": "actor", "Hair Color": "blonde",
                    "Age": 31, "Sex": "woman"},
                8: {"Name": "Nicholas Woodard", "Blood Type": "B+", "Occupation": "tailor", "Hair Color": "black",
                    "Age": 35, "Sex": "man"},
                9: {"Name": "Randall Hagan", "Blood Type": "O-", "Occupation": "nurse", "Hair Color": "blonde",
                    "Age": 47, "Sex": "man"},
                }

    with open("used_positions", 'rb') as f:
        used_positions = pickle.load(f)



    if run_number == 0:
        main_sus = random.choice(suspects)
        with open("main_sus", 'wb') as f:
            pickle.dump(main_sus, f)
            # question_numbers = pickle.load(f)


        with open("run_number", 'wb') as f:
            pickle.dump(run_number, f)
    else:
        with open("main_sus", 'rb') as f:
            main_sus = pickle.load(f)
        run_number+=1
        with open("run_number", 'wb') as f:
            pickle.dump(run_number, f)

    # print(main_sus)
    hints = [f"It was {random.choice(['Sunday', 'Monday', 'Tuesday', 'Thursday', 'Wednesday', 'Friday', 'Saturday'])}",
             f"The hair color was {main_sus['Hair Color']}",
             f"The guy had a mask in the elevator",
             f"The guy looked to be around {random.randint(main_sus['Age'] - 3, main_sus['Age'] + 5)}",
             f"I might put you off the scent :)",
             f"Not sure but {random.choice([main_sus['Hair Color'], 'black', 'blonde'])} hair color",
             f"maybe a scissor",
             f"When I was coming into the building I saw a {main_sus['Sex']}",
             f"He had strange cloths but I guess he was a man",
             f"Maybe she was a woman",
             f"They were fighting and suddenly they became silent",
             f"I know this neighbourhood very well",
             f"I'm not sure about hair color",
             f"it was around {random.randrange(1, 13)} {random.choice(['a.m', 'p.m'])}",
             f"the assassin had a knife or sth like that",
             f"I also heard {main_sus['Name'].split(' ')[0]} multiple times",
             f"I also heard {random.choice(['John', 'Elizabeth', 'Eric', 'Stephanie', 'Randall', 'Norma', 'Kathleen', 'Christina', 'Nicholas', 'David'])} multiple times",
             f"I heard the name {random.choice(['John', 'Elizabeth', 'Eric', 'Stephanie', 'Randall', 'Norma', 'Kathleen', 'Christina', 'Nicholas', 'David'])}",
             f"The test shows the blood type is {main_sus['Blood Type']}",
             f"I took a look at the corpse",
             f"You must believe me",
             f"The assassin is {main_sus['Occupation']}",
             f"The assassin is {random.choice(['tailor', 'butcher', 'nurse', 'actor', 'painter', 'surgeon', 'goldsmith', 'cook'])}",
             f"I think I have no more information",
             ]

    if main_sus['Occupation'] == 'surgeon':
        hints.append('The assassin knew how to use a knife ')
    elif main_sus['Occupation'] == 'tailor':
        hints.append('The assassin knew how to use a scissor ')
    elif main_sus['Occupation'] == "actor":
        hints.append('The assassin must like the art ')
    else:
        hints.append('The assassin was a noob')
    run_number
    return suspects, main_sus, hints, used_positions
