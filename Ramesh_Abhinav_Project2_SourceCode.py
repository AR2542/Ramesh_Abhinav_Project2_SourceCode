import random 

#The main method that begins the Cluedo game and setup
def start_game(players, keys):
    print("\n\nThere are 6 Players, from Player 0 to Player 5. Player 0 and Player 3 are Human, whereas the rest of them are AI!\n\n")
    print("\nWelcome to the Cluedo game! Your objective is to beat the computer in guessing the answer before they do!\n")
    answer_game, shuffle_deck = create_solution(game_characters.copy(), game_weapons.copy(), game_rooms.copy())
    print("The answer deck has been taken out!\n")
    print("The Answer consists of 3 cards: 1 Character Card, 1 Weapon Card and 1 Room/Location Card!\n")
    print("These Cards answer the Murder Mystery: Who did it? With what weapon? And in What room?\n")
    print("Now the rest of the cards will be shuffled among the players!\n")
    assign_cards(game_players, shuffle_deck)
    print("The cards have been shuffled!\n")
    create_log(players, suggestion_log)

    #This loop goes on until either someone gets a correct answer or everyone gets the accusation wrong
    while correct(character_accusation) != True and wrong(character_accusation) != len(game_characters):
        for i in keys:
            #Base Case: If player already made a wrong accusation, they cannot play
            if character_accusation[i] == "Wrong": 
                print(f"Player {i} has already made a wrong accusation! They cannot play. Going to next player.")
                continue
            #The while loop conditions inside just to avoid extra turns
            if correct(character_accusation) == True: break
            #If only 2 players are left (or 1 if the 5th player gets their accusation wrong in this scenario), the remaining will have to make an accusation 
            if wrong(character_accusation) >= 4: 
                direct_accuse(i, players, keys, answer_game)
                continue
            if wrong(character_accusation) == len(game_characters): break

            #Player rolls dice -> They play their turn -> They suggest or accuse or dont depend on where they are or preference
            input(f"\nPlayer {i}, press Enter to start the turn...\n")
            #dice_roll = random.randint(1, 6)
            #print(f"Player {i} rolled: {dice_roll}\n")
            if players[i]["Type"] == "Human":
                input(f"\nPlayer {i}, press Enter to roll dice...\n")
                dice_roll = random.randint(1, 6)
                print(f"Player {i} rolled: {dice_roll}\n")
                turn(i, players, dice_roll)
                suggest_or_accuse(i, players, keys, answer_game)
            elif players[i]["Type"] == "AI":
                dice_roll = random.randint(1, 6)
                print(f"Player {i} rolled: {dice_roll}\n")
                ai_turn(i, players, dice_roll)
                ai_suggest_or_accuse(i, players, keys, answer_game)

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
    rem = len(deck)%len(players)
    print(f"Remaining Cards after diving the deck size by number of players: {rem}")
    #Loop only goes till an even distribution till the smallest remainder
    while(len(deck) != rem):
        temp_assign = random.choice(deck)

        #If random choice is a character card, put it in the character section
        if temp_assign in game_characters:
            if temp_assign not in players[i%len(players)]["Cards"]["Character"]: players[i%len(players)]["Cards"]["Character"].append(temp_assign)

        #If random choice is a weapon card, put it in the weapon section
        elif temp_assign in game_weapons:
            if temp_assign not in players[i%len(players)]["Cards"]["Weapon"]: players[i%len(players)]["Cards"]["Weapon"].append(temp_assign)

        #If random choice is a room card, put it in the room section
        elif temp_assign in game_rooms:
            if temp_assign not in players[i%len(players)]["Cards"]["Room"]: players[i%len(players)]["Cards"]["Room"].append(temp_assign)

        #Make sure to remove card from deck once its assigned to a player
        deck.remove(temp_assign)

        i += 1
        
    print(f"Cards Left are: {deck}")
        
    #If rem is greater than 0 it means some cards are still left to be distributed
    if rem > 0:
        print("Some cards are still left! These cards will be distrbuted to everyone!\n")
        for i in game_players:
            for j in deck:
                if j in game_characters: game_players[i]["Cards"]["Character"].append(j)
                elif j in game_weapons: game_players[i]["Cards"]["Weapon"].append(j)
                elif j in game_rooms: game_players[i]["Cards"]["Room"].append(j)
    else: print("No cards left! Every non solution card has been succesfully distributed evenly!\n")

    for i in players:
        #Plot out the Possible cards (Basically cards not owned or seen) for AI players
        if players[i%len(players)]["Type"] == "AI": possible_card_sorter(players[i%len(players)])

#Baisc logic of possible cards: Whatever cards I dont have right now
def possible_card_sorter(player):
    temp_char = game_characters.copy()
    for card in player["Cards"]["Character"]:
        if card in temp_char: temp_char.remove(card)
    player["Possible"]["Characters"] = temp_char

    temp_weap = game_weapons.copy()
    for card in player["Cards"]["Weapon"]:
        if card in temp_weap: temp_weap.remove(card)
    player["Possible"]["Weapons"] = temp_weap

    temp_room = game_rooms.copy()
    for card in player["Cards"]["Room"]:
        if card in temp_room: temp_room.remove(card)
    player["Possible"]["Rooms"] = temp_room

#Initialize Empty Dictionaries for Human Players to see what suggestions they have made earlier and what cards they have got or not got
def create_log (players, suggestion_log):
    i = 0
    for j in players:
        if players[j]["Type"] == "Human":
            suggestion_log[i] = {"PlayerID": j, "Name": players[j]["Name"], "Suggestions": {}}
            i = i + 1

def insert_log(temp_char, temp_weap, temp_room, shown_card, player_name):
    for i in suggestion_log:
        if suggestion_log[i]["Name"] == player_name:
            temp = len(suggestion_log[i]["Suggestions"])
            if shown_card == temp_char: suggestion_log[i]["Suggestions"].update({temp + 1: {temp_char: "Shown", temp_weap: "Not Shown", temp_room: "Not Shown"}})
            elif shown_card == temp_weap: suggestion_log[i]["Suggestions"].update({temp + 1: {temp_char: "Not Shown", temp_weap: "Shown", temp_room: "Not Shown"}})
            elif shown_card == temp_room: suggestion_log[i]["Suggestions"].update({temp + 1: {temp_char: "Not Shown", temp_weap: "Not Shown", temp_room: "Shown"}})
            else: suggestion_log[i]["Suggestions"].update({temp + 1: {temp_char: "Not Shown", temp_weap: "Not Shown", temp_room: "Not Shown"}})

def show_log(suggestion_log, player_name):
    print("\nThese are the suggestion you have made so far!\n")
    for i in suggestion_log:
        if suggestion_log[i]["Name"] == player_name:
            for j in suggestion_log[i]["Suggestions"]:
                print(f"{j}: {suggestion_log[i]["Suggestions"][j]}")
    print("\n")

#Based on Dice Roll, the player moves from different rooms to other rooms. Turn ends if Player in any room or Dice roll becomes 0
def turn(id, players, dice):
    for number in range(dice):
        print(f"You are currently in {players[id]["Location"]}\n")
        print(f"Your cards are {players[id]["Cards"]}\n")
        can_go_to(players, id, players[id]["Location"])

        if(players[id]["Location"] != "Corridor"): break

#Based on Dice Roll, the AI player moves from different rooms to other rooms. Turn ends if Player in any room or Dice roll becomes 0
def ai_turn(id, players, dice):
    for number in range(dice):
        print(f"You are currently in {players[id]["Location"]}\n")
        print(f"Your cards are {players[id]["Cards"]}\n")
        ai_can_go_to(players, id, players[id]["Location"])

        if(players[id]["Location"] != "Corridor"): break
    
#Different Paths the players can go to. Default Paths: Hall -> Corridor -> Other rooms and vice versa. Secret Paths: Backyard -> Frontyard, Bedroom -> Storage and vice versa
def can_go_to(players, id, location):
    if location != "Corridor": 

        if location == "Backyard":
            option = input("Press 1 to go to Corridor. Press 2 for Secret Passage to Frontyard.\n")
            while option not in ['1', '2']:
              print("Invalid option! Please try again.\n")  
              option = input("Press 1 to go to Corridor. Press 2 for Secret Passage to Frontyard.\n")
            if int(option) == 1: players[id]["Location"] = "Corridor"
            else: players[id]["Location"] = "Frontyard"

        elif location == "Frontyard":
            option = input("Press 1 to go to Corridor. Press 2 for Secret Passage to Backyard.\n")
            while option not in ['1', '2']:
              print("Invalid option! Please try again.\n")  
              option = input("Press 1 to go to Corridor. Press 2 for Secret Passage to Backyard.\n")
            if int(option) == 1: players[id]["Location"] = "Corridor"
            else: players[id]["Location"] = "Backyard"

        elif location == "Bedroom":
            option = input("Press 1 to go to Corridor. Press 2 for Secret Passage to Storage.\n")
            while option not in ['1', '2']:
              print("Invalid option! Please try again.\n")  
              option = input("Press 1 to go to Corridor. Press 2 for Secret Passage to Storage.\n")
            if int(option) == 1: players[id]["Location"] = "Corridor"
            else: players[id]["Location"] = "Storage"

        elif location == "Storage":
            option = input("Press 1 to go to Corridor. Press 2 for Secret Passage to Bedroom.\n")
            while option not in ['1', '2']:
              print("Invalid option! Please try again.\n")  
              option = input("Press 1 to go to Corridor. Press 2 for Secret Passage to Bedroom.\n")
            if int(option) == 1: players[id]["Location"] = "Corridor"
            else: players[id]["Location"] = "Bedroom"

        else:
            option = input(f"You are in {location}! You can go to Corridor! Press 1 to go to Corridor\n")
            while option not in ['1']:
                print("Invalid option! Try again!\n")
                option = input(f"You are in {location}! You can go to Corridor! Press 1 to go to Corridor\n")

            players[id]["Location"] = "Corridor"
    else:
        for i in range(len(game_rooms)): print(f"{i}: {game_rooms[i]}. ")
        option = input("You are in Corridor! You have the following rooms to go to! Enter the respective number for the room you need to go to!\n")
        while option.isnumeric() != True or int(option) < 0 or int(option) > len(game_rooms) - 1:
            print("Invalid option! Try again!\n")
            for i in range(len(game_rooms)): print(f"{i}: {game_rooms[i]}. ")
            option = input("You are in Corridor! You have the following rooms to go to! Enter the respective number for the room you need to go to!\n")
        
        players[id]["Location"] = game_rooms[int(option)]
    
def ai_can_go_to(players, id, location):
    if location != "Corridor":
        total_rooms = len(players[id]["Cards"]["Room"]) + len(players[id]["Confirmed"]["Room"])
        if total_rooms == len(game_rooms): 
            players[id]["Location"] = "Corridor"
            print(f"Player {id} decided to go to the Corridor!\n")
        elif location == "Backyard":
            if "Frontyard" in players[id]["Cards"]["Room"] or "Frontyard" in players[id]["Confirmed"]["Room"]: 
                players[id]["Location"] = "Corridor"
                print(f"Player {id} decided to go to the Corridor!\n")
            else: 
                players[id]["Location"] = "Frontyard"
                print(f"Player {id} decided to go to the Frontyard! Their turn ends!\n")
        elif location == "Frontyard":
            if "Backyard" in players[id]["Cards"]["Room"] or "Backyard" in players[id]["Confirmed"]["Room"]: 
                players[id]["Location"] = "Corridor"
                print(f"Player {id} decided to go to the Corridor!\n")
            else: 
                players[id]["Location"] = "Backyard"
                print(f"Player {id} decided to go to the Backyard! Their turn ends!\n")
        elif location == "Bedroom":
            if "Storage" in players[id]["Cards"]["Room"] or "Storage" in players[id]["Confirmed"]["Room"]: 
                players[id]["Location"] = "Corridor"
                print(f"Player {id} decided to go to the Corridor!\n")
            else: 
                players[id]["Location"] = "Storage"
                print(f"Player {id} decided to go to the Storage! Their turn ends!\n")
        elif location == "Storage":
            if "Bedroom" in players[id]["Cards"]["Room"] or "Bedroom" in players[id]["Confirmed"]["Room"]: 
                players[id]["Location"] = "Corridor"
                print(f"Player {id} decided to go to the Corridor!\n")
            else: 
                players[id]["Location"] = "Bedroom"
                print(f"Player {id} decided to go to the Bedroom! Their turn ends!\n")
        else:
            players[id]["Location"] = "Corridor"
            print(f"Player {id} has decided to go to the Corridor!\n")
    else:
        temp_choice = game_rooms.copy()
        for card in players[id]["Cards"]["Room"]: 
            if card in temp_choice: temp_choice.remove(card)
        for card in players[id]["Confirmed"]["Room"]: 
            if card in temp_choice: temp_choice.remove(card)
        if len(temp_choice) == 0: temp_room = random.choice(game_rooms)
        else: temp_room = random.choice(temp_choice)
        players[id]["Location"] = temp_room
        print(f"Player {id} has decided to go to {temp_room}! Their turn ends!\n")

def suggest_or_accuse(id, players, keys, solution):
    print(f"Player {id}, you are currently in {players[id]["Location"]}!")
    if players[id]["Location"] != "Corridor": 
        option = input("Press 1 to make a suggestion, or Press 2 to make an accusation.\n")
        while option not in ['1', '2']:
            print("Invalid option. Please try again.\n")
            option = input("Press 1 to make a suggestion, or Press 2 to make an accusation.\n")
        if int(option) == 1:
            print(f"Player {id} is making a suggestion!\n")
            show_log(suggestion_log, players[id]["Name"])
            char_option, temp_char, temp_weap, temp_room = guess(id, players, keys)
            players[char_option]["Location"] = players[id]["Location"]
            print(f"Player {id} suggests it was {temp_char}, who did it with {temp_weap}, in {temp_room}\n")
            print(f"Player {[char_option]}, who is, {temp_char} has been moved to {temp_room}\n")

            card_showing_round(id, players, temp_char, temp_weap, temp_room)
        else:
            print(f"Player {id} is making an accusation!")
            temp_char, temp_weap, temp_room = accuse(id, players, keys)
            if temp_char in solution["Answer Character"] and temp_weap in solution["Answer Weapon"] and temp_room in solution["Answer Room"]: 
                character_accusation[id] = "Correct"
                print(f"Player {id} has guessed the answer correctly! {temp_char}, {temp_weap}, {temp_room}. The game has ended!\n")
            else:
                character_accusation[id] = "Wrong"
                print(f"Player {id} guessed incorrectly, and is disqualified for the game!\n")
                
def ai_suggest_or_accuse(id, players, keys, solution):
    if players[id]["Location"] != "Corridor":
        if len(players[id]["Confirmed"]["Character"]) == 1 and len(players[id]["Confirmed"]["Weapon"]) == 1 and len(players[id]["Confirmed"]["Room"]) == 1:
            print(f"Player {id} has decided make an accusation!\n")
            temp_char, temp_weap, temp_room = players[id]["Confirmed"]["Character"][0], players[id]["Confirmed"]["Weapon"][0], players[id]["Confirmed"]["Room"][0]
            if temp_char in solution["Answer Character"] and temp_weap in solution["Answer Weapon"] and temp_room in solution["Answer Room"]:
                character_accusation[id] = "Correct"
                print(f"Player {id} has guessed the answer correctly! {temp_char}, {temp_weap}, {temp_room}. The game has ended!\n")
            else:
                character_accusation[id] = "Wrong"
                print(f"Player {id} guessed incorrectly, and is disqualified for the game!\n")
                
        else:
            print(f"Player {id} has decided to make a suggestion!\n")
            char_option, temp_char, temp_weap, temp_room = ai_guess(id, players)
            players[char_option]["Location"] = players[id]["Location"]
            print(f"Player {id} suggests it was {temp_char}, who did it with {temp_weap}, in {temp_room}\n")
            print(f"Player {[char_option]}, who is, {temp_char} has been moved to {temp_room}\n")

            card_showing_round(id, players, temp_char, temp_weap, temp_room)
            
#Function for suggesting that asks the player the suggested character and weapon, and assumes the same location as they are in
def guess(id, players, keys):
    print(f"Your cards are {players[id]["Cards"]}")
    for i in keys: print(f"{i}: {game_characters[i]}. ")
    char_option = input("Pick a number to guess which character you think is the murderer!\n")
    while char_option.isnumeric() != True or int(char_option) < 0 or int(char_option) > len(keys) - 1:
        print("Invalid option. Please try again!\n")
        for i in keys: print(f"{i}: {game_characters[i]}. ")
        char_option = input("Pick a number to guess which character you think is the murderer!\n")
    temp_char = players[int(char_option)]["Name"]

    for i in keys: print(f"{i}: {game_weapons[i]}. ")
    weap_option = input("Select the weapon with which the murder took place. Enter a number from the give range of options!\n")
    while weap_option.isnumeric() != True or int(weap_option) < 0 or int(weap_option) > len(game_weapons) - 1:
        print("Invalid option. Please try again.\n")
        for i in keys: print(f"{i}: {game_weapons[i]}. ")
        weap_option = input("Select the weapon with which the murder took place. Enter a number from the give range of options!\n")
    temp_weap = game_weapons[int(weap_option)]

    temp_loc = players[id]["Location"]
    return int(char_option), temp_char, temp_weap, temp_loc

#Function for accusation that asks the character who is the murderer, with what weapon and which location
def accuse(id, players, keys):
    print(f"Your cards are {players[id]["Cards"]}")
    for i in keys: print(f"{i}: {game_characters[i]}. ")
    char_option = input("Pick a number to guess which character you think is the murderer!\n")
    while char_option.isnumeric() != True or int(char_option) < 0 or int(char_option) > len(game_characters) - 1:
        print("Invalid option. Please try again!\n")
        for i in keys: print(f"{i}: {game_characters[i]}. ")
        char_option = input("Pick a number to guess which character you think is the murderer!\n")
    temp_char = players[int(char_option)]["Name"]

    for i in keys: print(f"{i}: {game_weapons[i]}. ")
    weap_option = input("Select the weapon with which the murder took place. Enter a number from the give range of options!\n")
    while weap_option.isnumeric() != True or int(weap_option) < 0 or int(weap_option) > len(game_weapons) - 1:
        print("Invalid option. Please try again.\n")
        for i in keys: print(f"{i}: {game_weapons[i]}. ")
        weap_option = input("Select the weapon with which the murder took place. Enter a number from the give range of options!\n")
    temp_weap = game_weapons[int(weap_option)]

    for i in range(len(game_rooms)): print(f"{i}: {game_rooms[i]}. ")
    room_option = input("Select the location where the murder took place!\n")
    while room_option.isnumeric() != True or int(room_option) < 0 or int(room_option) > len(game_rooms) - 1:
        print("Invalid option. Please try again.\n")
        for i in game_rooms: print(f"{i}: {game_rooms[i]}. ")
        room_option = input("Select the location where the murder took place!\n")
    temp_room = game_rooms[int(room_option)]
    return temp_char, temp_weap, temp_room

def ai_guess(id, players):
    if len(players[id]["Possible"]["Characters"]) == 0: 
        if len(players[id]["Confirmed"]["Character"]) == 1:
            temp_char = random.choice(players[id]["Confirmed"]["Character"])
        else: temp_char = random.choice(players[id]["Cards"]["Character"])
    else: temp_char = random.choice(players[id]["Possible"]["Characters"])
    #print(f"Guess Character: {temp_char}\n")
    char_option = 0
    for char in players:
        if players[char]["Name"] == temp_char:
            #print("Character Found!")
            char_option = char
            break
    if len(players[id]["Possible"]["Weapons"]) == 0: 
        if len(players[id]["Confirmed"]["Weapon"]) == 1:
            temp_weap = random.choice(players[id]["Confirmed"]["Weapon"])
        else: temp_weap = random.choice(players[id]["Cards"]["Weapon"])
    else: temp_weap = random.choice(players[id]["Possible"]["Weapons"])
    temp_room = players[id]["Location"]

    return char_option, temp_char, temp_weap, temp_room

#If only 2 players are left, this method is called and both players have to make a final accusation
def direct_accuse(id, players, keys, solution):
    print("There are not enough players left to play! So you have to make an accusation now!")
    if players[id]["Type"] == "Human":
        temp_char, temp_weap, temp_room = accuse(id, players, keys)
        if temp_char in solution["Answer Character"] and temp_weap in solution["Answer Weapon"] and temp_room in solution["Answer Room"]: 
            character_accusation[id] = "Correct"
            print(f"Player {id} has guessed the answer correctly! {temp_char}, {temp_weap}, {temp_room}. The game has ended!\n")
        else:
            character_accusation[id] = "Wrong"
            print(f"Player {id} guessed incorrectly, and is disqualified for the game!\n")
    else:
        if len(players[id]["Confirmed"]["Character"]) == 1: temp_char = players[id]["Confirmed"]["Character"][0]
        elif len(players[id]["Possible"]["Characters"]) >= 1: temp_char = random.choice(players[id]["Possible"]["Characters"])

        if len(players[id]["Confirmed"]["Weapon"]) == 1: temp_weap = players[id]["Confirmed"]["Weapon"][0]
        elif len(players[id]["Possible"]["Weapons"]) >= 1: temp_weap = random.choice(players[id]["Possible"]["Weapons"])

        if len(players[id]["Confirmed"]["Room"]) == 1: temp_room = players[id]["Confirmed"]["Room"][0]
        elif len(players[id]["Possible"]["Rooms"]) >= 1: temp_room = random.choice(players[id]["Possible"]["Rooms"])

        if temp_char in solution["Answer Character"] and temp_weap in solution["Answer Weapon"] and temp_room in solution["Answer Room"]:
                character_accusation[id] = "Correct"
                print(f"Player {id} has guessed the answer correctly! {temp_char}, {temp_weap}, {temp_room}. The game has ended!\n")
        else:
            character_accusation[id] = "Wrong"
            print(f"Player {id} guessed incorrectly, and is disqualified for the game!\n")

#After every suggestion, the game goes in a sequence to check if any players have cards that the original player (whose turn it is) suggested
def card_showing_round(id, players, temp_char, temp_weap, temp_room):
    i = id
    i = i + 1
    while i%len(players) != id:
        #If Player does not have any cards to show from the suggestion, basically 0 out of the 3 suggested cards: Character, Weapon, Room
        if temp_char not in players[i%len(players)]["Cards"]["Character"] and temp_weap not in players[i%len(players)]["Cards"]["Weapon"] and temp_room not in players[i%len(players)]["Cards"]["Room"]: 
            print(f"Player {i%len(players)} does not have any cards to show. Going to next Player\n")

            #If no one showed any card 
            if (i-1)%len(players) == id: insert_log(temp_char, temp_weap, temp_room, "", players[id]["Name"])
        #If a Player even has 1 out of 3, they need to show it if their turn comes
        else:
            print(f"Player {i%len(players)} decided to show cards to Player {id}!\n")
            #If Player has the character card same as the suggestion
            if temp_char in players[i%len(players)]["Cards"]["Character"]:
                #Player showing character card to Human Player
                if players[id]["Type"] == "Human":
                    if temp_char not in players[id]["Cards"]["Character"]: 
                        players[id]["Cards"]["Character"].append(temp_char)
                        insert_log(temp_char, temp_weap, temp_room, temp_char, players[id]["Name"])
                        #This statement is for records, basically an indication that the player actually got something
                        print(f"Player {i%len(players)} showed {temp_char} card to Player {id}!\n")
                #Player showing character card to AI Player
                elif players[id]["Type"] == "AI": 
                    #If AI hasnt seen this card before, it will remove it from the Possible section
                    if temp_char in players[id]["Possible"]["Characters"]: players[id]["Possible"]["Characters"].remove(temp_char)
                    #If character card not already registered by the AI as seen, then update the character card to its records
                    if temp_char not in players[id]["Cards"]["Character"]: 
                        players[id]["Cards"]["Character"].append(temp_char)
                        print(f"Player {i%len(players)} showed {temp_char} card to Player {id}!\n")
                    #If AI has seen all but 1 character card, and it hasnt confirmed on an answer yet, that means the final card in the Possible section must be the answer
                    if len(players[id]["Cards"]["Character"]) == len(game_characters) - 1  and len(players[id]["Confirmed"]["Character"]) == 0: 
                        temp = players[id]["Possible"]["Characters"].pop(0)
                        players[id]["Confirmed"]["Character"].append(temp)
                break
            #If Player has the weapon card same as the suggestion
            elif temp_weap in players[i%len(players)]["Cards"]["Weapon"]:
                #Player showing weapon card to Human Player
                if players[id]["Type"] == "Human":
                    if temp_weap not in players[id]["Cards"]["Weapon"]: 
                        players[id]["Cards"]["Weapon"].append(temp_weap)
                        insert_log(temp_char, temp_weap, temp_room, temp_weap, players[id]["Name"])

                        print(f"Player {i%len(players)} showed {temp_weap} card to Player {id}!\n")
                #Player showing weapon card to AI Player
                elif players[id]["Type"] == "AI":
                    #If AI hasnt seen this card before, it will remove it from the Possible section
                    if temp_weap in players[id]["Possible"]["Weapons"]: players[id]["Possible"]["Weapons"].remove(temp_weap)
                    #If weapon card not already registered by the AI as seen, then update the character card to its records
                    if temp_weap not in players[id]["Cards"]["Weapon"]: 
                        players[id]["Cards"]["Weapon"].append(temp_weap)
                        print(f"Player {i%len(players)} showed {temp_weap} card to Player {id}!\n")
                    #If AI has seen all but 1 weapon card, and it hasnt confirmed on an answer yet, that means the final card in the Possible section must be the answer
                    if len(players[id]["Cards"]["Weapon"]) == len(game_weapons) - 1  and len(players[id]["Confirmed"]["Weapon"]) == 0: 
                        temp = players[id]["Possible"]["Weapons"].pop(0)
                        players[id]["Confirmed"]["Weapon"].append(temp)
                break
            elif temp_room in players[i%len(players)]["Cards"]["Room"]:
                #Player showing room card to Human Player
                if players[id]["Type"] == "Human":
                    if temp_room not in players[id]["Cards"]["Room"]: 
                        players[id]["Cards"]["Room"].append(temp_room)
                        insert_log(temp_char, temp_weap, temp_room, temp_room, players[id]["Name"])

                        print(f"Player {i%len(players)} showed {temp_room} card to Player {id}!\n")
                #Human Player showing room card to AI Player
                elif players[id]["Type"] == "AI":
                    #If AI hasnt seen this card before, it will remove it from the Possible section
                    if temp_room in players[id]["Possible"]["Rooms"]: players[id]["Possible"]["Rooms"].remove(temp_room)
                    #If room card not already registered by the AI as seen, then update the character card to its records
                    if temp_room not in players[id]["Cards"]["Room"]: 
                        players[id]["Cards"]["Room"].append(temp_room)
                        print(f"Player {i%len(players)} showed {temp_room} card to Player {id}!\n")
                    #If AI has seen all but 1 room card, and it hasnt confirmed on an answer yet, that means the final card in the Possible section must be the answer
                    if len(players[id]["Cards"]["Room"]) == len(game_rooms) - 1  and len(players[id]["Confirmed"]["Room"]) == 0: 
                        temp = players[id]["Possible"]["Rooms"].pop(0)
                        players[id]["Confirmed"]["Room"].append(temp)
                break
        i = i + 1

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

game_players = {0: {"ID": 0, "Name": "Miss Scarlett", "Location": "Hall", "Cards": {"Character": [], "Weapon": [], "Room": []}, "Type": "Human"}, 
                1: {"ID": 1, "Name": "Colonel Mustard", "Location": "Hall", "Cards": {"Character": [], "Weapon": [], "Room": []}, "Type": "Human", "Possible": {"Characters": [], "Weapons": [], "Rooms": []}, "Confirmed": {"Character": [], "Weapon": [], "Room": []}}, 
                2: {"ID": 2, "Name": "Mrs. White", "Location": "Hall", "Cards": {"Character": [], "Weapon": [], "Room": []}, "Type": "Human", "Possible": {"Characters": [], "Weapons": [], "Rooms": []}, "Confirmed": {"Character": [], "Weapon": [], "Room": []}},
                3: {"ID": 3, "Name": "Reverend Green", "Location": "Hall", "Cards": {"Character": [], "Weapon": [], "Room": []}, "Type": "Human"},
                4: {"ID": 4, "Name": "Mrs. Peacock", "Location": "Hall", "Cards": {"Character": [], "Weapon": [], "Room": []}, "Type": "Human", "Possible": {"Characters": [], "Weapons": [], "Rooms": []}, "Confirmed": {"Character": [], "Weapon": [], "Room": []}},
                5: {"ID": 5, "Name": "Professor Plum", "Location": "Hall", "Cards": {"Character": [], "Weapon": [], "Room": []}, "Type": "AI", "Possible": {"Characters": [], "Weapons": [], "Rooms": []}, "Confirmed": {"Character": [], "Weapon": [], "Room": []}}}

#Stores the ids of the players in the form of [0, 1, 2, 3, 4, 5]
game_keys = list(game_players.keys())
#Used to store the accusation results either "Correct" or "Wrong". Initially looks like [None, None, None, None, None, None]
character_accusation = {}
for i in game_keys:
    character_accusation[i] = None

#Record that stores the suggestions made and cards shown/not shown for human players. Shown every turn
suggestion_log = {}

start_game(game_players, game_keys)
