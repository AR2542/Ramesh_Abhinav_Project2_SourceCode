#Random module used to select a card or roll a dice
import random 

#The main method that begins the Cluedo game and setup
def start_game(players, keys):
    answer_game, shuffle_deck = create_solution(game_characters.copy(), game_weapons.copy(), game_rooms.copy())
    print("The answer deck has been taken out!\n")
    assign_cards(game_players, shuffle_deck)
    print("The cards have been shuffled!\n")

    #This loop goes on until either someone gets a correct answer or everyone gets the accusation wrong
    while correct(character_accusation) != True and wrong(character_accusation) != len(game_characters):
        for i in keys:
            #Base Case: If player already made a wrong accusation, they cannot play
            if character_accusation[i] == "Wrong": continue
            #The while loop conditions inside just to avoid extra turns
            if correct(character_accusation) == True: break
            if wrong(character_accusation) == len(game_characters): break

            #Player rolls dice -> They play their turn -> They suggest or accuse or dont depend on where they are
            input(f"Player {i}, press Enter to roll dice...\n")
            dice_roll = random.randint(1, 6)
            print(f"Player {i} rolled: {dice_roll}\n")
            turn(i, players, dice_roll)
            suggest_or_accuse(i, players, keys, answer_game)
        
#Randomly make an answer deck of 1 Character card, 1 Weapon card, 1 Room card and remove them from the shuffling deck
def create_solution(characters, weapons, rooms):
    solution_character = random.choice(characters)
    solution_weapon = random.choice(weapons)
    solution_room = random.choice(rooms)

    solution_deck = {}
    solution_deck["Answer Character"] = solution_character
    solution_deck["Answer Weapon"] = solution_weapon
    solution_deck["Answer Room"] = solution_room

    print("The solution is: ", solution_deck, "\n")

    characters.remove(solution_character)
    weapons.remove(solution_weapon)
    rooms.remove(solution_room)

    return solution_deck, characters + weapons + rooms

#Give equal number of cards to player from the non answer deck
def assign_cards(players, deck):
    i = 0
    while(len(deck) != 0):
        temp_assign = random.choice(deck)
        temp_list = players[i%len(players)]["Cards"]
        temp_list.append(temp_assign)
        players[i%len(players)]["Cards"] = temp_list
        deck.remove(temp_assign)
        i += 1

#Based on Dice Roll, the player moves from different rooms to other rooms. Turn ends if Player in any room
def turn(id, players, dice):
    for number in range(dice):
        print(f"You are currently in {players[id]["Location"]}")
        can_go_to(players, id, players[id]["Location"])

        if(players[id]["Location"] != "Corridor"): break

#Different Paths the players can go to. Default Paths: Hall -> Corridor -> Other rooms and vice versa. Secret Paths: Backyard -> Frontyard, Bedroom -> Storage and vice versa
def can_go_to(players, id, location):
    if location != "Corridor": 

        if location == "Backyard":
            option = int(input("Press 1 to go to Corridor. Press 2 for Secret Passage to Frontyard.\n"))
            while option != 1 and option != 2:
              print("Invalid option! Please try again.")  
              option = int(input("Press 1 to go to Corridor. Press 2 for Secret Passage to Frontyard.\n"))
            if option == 1: players[id]["Location"] = "Corridor"
            else: players[id]["Location"] = "Frontyard"

        elif location == "Frontyard":
            option = int(input("Press 1 to go to Corridor. Press 2 for Secret Passage to Backyard.\n"))
            while option != 1 and option != 2:
              print("Invalid option! Please try again.")  
              option = int(input("Press 1 to go to Corridor. Press 2 for Secret Passage to Backyard.\n"))
            if option == 1: players[id]["Location"] = "Corridor"
            else: players[id]["Location"] = "Backyard"

        elif location == "Bedroom":
            option = int(input("Press 1 to go to Corridor. Press 2 for Secret Passage to Storage.\n"))
            while option != 1 and option != 2:
              print("Invalid option! Please try again.")  
              option = int(input("Press 1 to go to Corridor. Press 2 for Secret Passage to Storage.\n"))
            if option == 1: players[id]["Location"] = "Corridor"
            else: players[id]["Location"] = "Storage"

        elif location == "Storage":
            option = int(input("Press 1 to go to Corridor. Press 2 for Secret Passage to Bedroom.\n"))
            while option != 1 and option != 2:
              print("Invalid option! Please try again.")  
              option = int(input("Press 1 to go to Corridor. Press 2 for Secret Passage to Bedroom.\n"))
            if option == 1: players[id]["Location"] = "Corridor"
            else: players[id]["Location"] = "Bedroom"

        else:
            option = int(input(f"You are in {location}! You can go to Corridor! Press 1 to go to Corridor\n"))
            while option != 1:
                print("Invalid option! Try again!")
                option = int(input(f"You are in {location}! You can go to Corridor! Press 1 to go to Corridor\n"))

            players[id]["Location"] = "Corridor"
    else:
        for i in range(len(game_rooms)): print(f"{i+1}: {game_rooms[i]}. ")
        option = int(input("You are in Corridor! You have the following rooms to go to! Enter the respective number for the room you need to go to!\n"))
        while option < 1 or option > 9:
            print("Invalid option! Try again!")
            for i in range(len(game_rooms)): print(f"{i+1}: {game_rooms[i]}. ")
            option = int(input("You are in Corridor! You have the following rooms to go to! Enter the respective number for the room you need to go to!\n"))

        if option == 1: players[id]["Location"] = "Hall"
        if option == 2: players[id]["Location"] = "Kitchen"
        if option == 3: players[id]["Location"] = "Bedroom"
        if option == 4: players[id]["Location"] = "Ballroom"
        if option == 5: players[id]["Location"] = "Bathroom"
        if option == 6: players[id]["Location"] = "Dining"
        if option == 7: players[id]["Location"] = "Backyard"
        if option == 8: players[id]["Location"] = "Frontyard"
        if option == 9: players[id]["Location"] = "Storage"

#Function that controls players's suggestion and accusation. If player makes suggestion and any non solution deck card is in their suggestion, the first one gets added (Order based on Character -> Weapon -> Room)
def suggest_or_accuse(id, players, keys, solution):
    if players[id]["Location"] == "Hall": 
        option = int(input("Press 1 to make a suggestion, or Press 2 to make an accusation.\n"))
        while option != 1 and option != 2:
            print("Invalid option. Please try again.")
            option = int(input("Press 1 to make a suggestion, or Press 2 to make an accusation.\n"))
        if option == 1:
            char_option, temp_char, temp_weap, temp_loc = guess(id, players, keys)
            players[char_option]["Location"] = players[id]["Location"]
            print(f"Player {id} suggests it was {temp_char}, who did it with {temp_weap}, in {temp_loc}")
            print(f"Player {[char_option]}, who is, {temp_char} has been moved to {temp_loc}\n")

            if temp_char not in solution["Answer Character"]: 
                temp_list = players[id]["Cards"]
                temp_list.append(temp_char)
                players[id]["Cards"] = temp_list
            elif temp_weap not in solution["Answer Weapon"]:
                temp_list = players[id]["Cards"]
                temp_list.append(temp_weap)
                players[id]["Cards"] = temp_list
            elif temp_loc not in solution["Answer Room"]:
                temp_list = players[id]["Cards"]
                temp_list.append(temp_loc)
                players[id]["Cards"] = temp_list
        
        #If accusation is correct, the charcater_accusation record gets updated and used to end the game. Otherwise, player gets disqualified
        if option == 2:
            char_option, temp_char, temp_weap, temp_loc = accuse(id, players, keys)
            if temp_char in solution["Answer Character"] and temp_weap in solution["Answer Weapon"] and temp_loc in solution["Answer Room"]: 
                character_accusation[id] = "Correct"
                print(f"Player {id} has guessed the answer correctly! {temp_char}, {temp_weap}, {temp_loc}. The game has ended!")
            else:
                character_accusation[id] = "Wrong"
                print(f"Player {id} guessed incorrectly, and is disqualified for the game!")

    #Accusations can only be made in Hall. So from other rooms, players can only suggest          
    elif players[id]["Location"] != "Hall" and players[id]["Location"] != "Corridor":
        option = int(input("Press 1 to make a suggestion.\n"))
        while option != 1:
            print("Invalid option. Please try again.")
            option = int(input("Press 1 to make a suggestion.\n"))
        char_option, temp_char, temp_weap, temp_loc = guess(id, players, keys)
        players[char_option]["Location"] = players[id]["Location"]
        print(f"Player {id} suggests it was {temp_char}, who did it with {temp_weap}, in {temp_loc}")
        print(f"Player {[char_option]}, who is, {temp_char} has been moved to {temp_loc}\n")

        if temp_char not in solution["Answer Character"]: 
            temp_list = players[id]["Cards"]
            temp_list.append(temp_char)
            players[id]["Cards"] = temp_list
        elif temp_weap not in solution["Answer Weapon"]:
            temp_list = players[id]["Cards"]
            temp_list.append(temp_weap)
            players[id]["Cards"] = temp_list
        elif temp_loc not in solution["Answer Room"]:
            temp_list = players[id]["Cards"]
            temp_list.append(temp_loc)
            players[id]["Cards"] = temp_list

#Function for suggesting that asks the player the suggested character and weapon, and assumes the same location as they are in
def guess(id, players, keys):
    print(f"Your cards are {players[id]["Cards"]}")
    for i in keys: print(f"{i}: {game_characters[i]}. ")
    char_option = int(input("Pick a number to guess which character you think is the murderer!\n"))
    while char_option > keys[len(keys) - 1] or char_option < keys[0]:
        print("Invalid option. Please try again!")
        for i in keys: print(f"{i}: {game_characters[i]}. ")
        char_option = int(input("Pick a number to guess which character you think is the murderer!\n"))
    temp_char = players[char_option]["Name"]

    for i in keys: print(f"{i}: {game_weapons[i]}. ")
    weap_option = int(input("Select the weapon with which the murder took place. Enter a number from the give range of options!\n"))
    while weap_option < 0 or weap_option > 5:
        print("Invalid option. Please try again.")
        for i in keys: print(f"{i}: {game_weapons[i]}. ")
        weap_option = int(input("Select the weapon with which the murder took place. Enter a number from the give range of options!\n"))
    temp_weap = game_weapons[weap_option]

    temp_loc = players[id]["Location"]
    return char_option, temp_char, temp_weap, temp_loc

#Function for accusation that asks the character who is the murderer, with what weapon and which location
def accuse(id, players, keys):
    print(f"Your cards are {players[id]["Cards"]}")
    for i in keys: print(f"{i}: {game_characters[i]}. ")
    char_option = int(input("Pick a number to guess which character you think is the murderer!\n"))
    while char_option > keys[len(keys) - 1] or char_option < keys[0]:
        print("Invalid option. Please try again!")
        for i in keys: print(f"{i}: {game_characters[i]}. ")
        char_option = int(input("Pick a number to guess which character you think is the murderer!\n"))
    temp_char = players[char_option]["Name"]

    for i in keys: print(f"{i}: {game_weapons[i]}. ")
    weap_option = int(input("Select the weapon with which the murder took place. Enter a number from the give range of options!\n"))
    while weap_option < 0 or weap_option > 5:
        print("Invalid option. Please try again.")
        for i in keys: print(f"{i}: {game_weapons[i]}. ")
        weap_option = int(input("Select the weapon with which the murder took place. Enter a number from the give range of options!\n"))
    temp_weap = game_weapons[weap_option]

    for i in range(len(game_rooms)): print(f"{i}: {game_rooms[i]}. ")
    loc_option = int(input("Select the location where the murder took place!\n"))
    while loc_option < 0 and loc_option > 8:
        print("Invalid option. Please try again.")
        for i in game_rooms: print(f"{i}: {game_rooms[i]}. ")
        loc_option = int(input("Select the location where the murder took place!\n"))
    temp_loc = game_rooms[loc_option]
    return char_option, temp_char, temp_weap, temp_loc

#Finds if anyone has made a correct accusation. If yes, then used to end the game
def correct(accusation):
    for i in accusation:
        if accusation[i] == "Correct": return True
    return False

#Finds out how many people have accused wrongly. If the number is the same as the number of players, then used to end the game
def wrong(accusation):
    count = 0
    for i in accusation: 
        if accusation[i] == "Wrong": count += 1
    return count

#All the cards used in the game
game_characters = ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Reverend Green", "Mrs. Peacock", "Professor Plum"]
game_weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
game_rooms = ["Hall", "Kitchen", "Bedroom", "Ballroom", "Bathroom", "Dining", "Backyard", "Frontyard", "Storage"]

#All the Players who will play. Here, they dont have any cards
game_players = {0: {"Name": "Miss Scarlett", "Location": "Hall", "Cards": []}, 1: {"Name": "Colonel Mustard", "Location": "Hall", "Cards": []}, 2: {"Name": "Mrs. White", "Location": "Hall", "Cards": []}, 3: {"Name": "Reverend Green", "Location": "Hall", "Cards": []}, 4: {"Name": "Mrs. Peacock", "Location": "Hall", "Cards": []}, 5: {"Name": "Professor Plum", "Location": "Hall", "Cards": []}}
#Stores the ids of the players in the form of [0, 1, 2, 3, 4, 5]
game_keys = list(game_players.keys())
#Used to store the accusation results either "Correct" or "Wrong". Initially looks like [None, None, None, None, None, None]
character_accusation = {}
for i in game_keys:
    character_accusation[i] = None

#Begins the game with the players
start_game(game_players, game_keys)