# Ramesh_Abhinav_Project2_SourceCode

## Description
This program replicates the well known Cluedo game which comes under the category of "Murder Mystery". This README file will give an explanation of what each methods are supposed to do, the data structures and how to run the program.

## Methods
At the top of the program (below the "import random" statement), the first method is the start_game(players, keys) method that basically gets the setup of the game by doing the following:
    1. First it creates a solution deck and separates it from the shuffling deck by calling on the create_solution(characts, weapons, rooms) method
    2. Then it distributes the shuffling deck evenly with the assign_cards(players, deck) method, among the 6 players. Here, I have gone with the scenario that all shuffling cards can be evenly distributed among players.
    3. After that, the while loop starts, which only stops if: Someone gets an answer correct, or Everyone gets the answer wrong.
    4. Inside the while loop, there is a dice roll starting with the 1st player between 1 and 6, and the turn(id, players, dice) is called. After the player has done their moves, the suggest_or_accuse(id, players, keys, solution) is called in order to see if the player is in the room to make a suggestion or accusation.

Now I will go over each method referred in the above part and also talk about the methods that are called by these methods.

### create_solution(characts, weapons, rooms)
This method picks one random card from the character deck, weapon deck and room deck each and considers them to be the final answer to the mystery. The rest of the cards are combined into a shuffle deck and returned as output along with the solution deck.

### assign_cards(players, deck)
This method is used to distribute the shuffling deck among the players. Usually every player should get the same number of cards and if there are still cards left in the shuffling deck, its given as clues to everyone. This program is written with the assumption that the total number of cards that are left after taking out the solution is evenly distributable.

### turn(id, players, dice)
Taking the Player's id (basically whose turn it is) and the dice roll, the player basically makes their move. Everyone starts from the same room which is the Hall, and from the Hall, they can only get to the Corridor. From the Corridor, every room is accessible, even the Hall. There are some rooms which have a secret passage, but those are only accessible to the players if they are in those specific rooms when the turn begins. If a player's dice roll ends while they are in the corridor, they have to wait for the next turn to get to a room. If a player gets in a room, even if they have some dice roll left, the turn ends and the game moves to the next method.

### suggest_or_accuse(id, players, keys, solution)
This is the main gameplay. Players make suggestions or accusations and get clues in the form or cards added to their inventory without others knowing, or the game ending based on aforementioned conditions in the Methods header, point 3. Players cannot make a suggestion in the Corridor, they have to be in one of the 9 rooms defined in this program to be able to make a suggestion. If a player wishes to make an accusation, they strictly can do so only if they are in the Hall, basically where they start from. Here's how a suggestion and an accusation works:
    - If a player wants to make a suggestion, they have to only answer which character they think could have done it, and with what weapon. The room they are in will be considered as the location. And whoever they think could have done the murder, that player will be shifted to the same room as the player. If any card from the player's guesses is in circulation (or not in the solution), only one of them will be added to the player's card inventory. No player will know what card was given to the player, and this program works in a way where the new card will be displayed at the next turn. If no card is added (meaning none of the cards were in circulation), then the turn ends as well.
    - If a player wants to make an accusation, they have to end their turn by getting into the Hall. Once they arrive at the Hall, they have the option to either make a suggestion or make an accusation. If they choose the former, refer to above point. If they choose the latter, then the player has to answer all 3 parts: Which character did it? With what weapon? And which location? If the player says it correctly, the solution it shown to everyone and the game ends. If the player guesses even one wrongly, the answer is not disclosed (nor the player's guess), and the player is disqualified and they wont be able to play until the game ends.

### can_go_to(players, id, location)
This is a method that is used inside the turn(id, players, dice) method. The player has a starting point and they are able to go to other rooms in the following order:
Hall -> Corridor (Initially)
Corridor -> Every room

For every A -> B, the vice versa that is, B -> A is also true.

Once the player gets to any room from the Corridor, the turn ends. Even if their dice roll is still more than 0.

There are some secret passages that can be used if the player starts their turn from one of those rooms.
Backyard -> Frontyard (Vice Versa applies too)
Bedroom -> Storage (Vice Versa applies too)

These secret passages can help a player get to some rooms directly without going to corridor again. 
Once the turn ends, the player's location is updated.

### guess(id, players, keys)
This is a method that is used in the suggestion case. The player is only asked to name the character and the weapon.

### accuse(id, players, keys)
Similar to the guess method, this method is used in the accusation case. The player is asked to name the character, the weapon and the room where it happened.

### correct(accusation)
A small method that checks the accusation record of every player if anyone has guessed the answer correctly. If it finds any, it is used to end the game.

### wrong(accusation)
Another small method that counts how many people have made the wrong accusation. This method is used to end the game if the number of people who got their accusation wrong is the same as the number of players (everyone got it wrong).

## Data Structures
There are 3 Lists that store the total characters, weapons and rooms used in the deck.
game_characters = ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Reverend Green", "Mrs. Peacock", "Professor Plum"]
game_weapons = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]
game_rooms = ["Hall", "Kitchen", "Bedroom", "Ballroom", "Bathroom", "Dining", "Backyard", "Frontyard", "Storage"]

There are 6 Character Cards, 6 Weapon Cards and 9 Room Cards. 1 of each category is taken out to form the solution, making the total remaining cards: 6 + 6 + 9 - 3 = 18. These 18 crds are divided among 6 players, so every player gets 3 cards.

This is a dictionary that stores the records of the players as the game goes on. Initially, every player is in the Hall and no one has any cards. When start_game(players, keys) is called, 3 cards are assigned to each player.
game_players = {0: {"Name": "Miss Scarlett", "Location": "Hall", "Cards": []}, 1: {"Name": "Colonel Mustard", "Location": "Hall", "Cards": []}, 2: {"Name": "Mrs. White", "Location": "Hall", "Cards": []}, 3: {"Name": "Reverend Green", "Location": "Hall", "Cards": []}, 4: {"Name": "Mrs. Peacock", "Location": "Hall", "Cards": []}, 5: {"Name": "Professor Plum", "Location": "Hall", "Cards": []}}

A list that stores the keys of the nested dictionary. Used for easy iteration.
game_keys = list(game_players.keys())

This dictionary stores the accusation records of each player. Initially all values are None.
character_accusation = {}

## How to play the game in this program?
The game starts with the line at the very end of the code: start_game(game_players, game_keys) and the first input starts with the interpreter asking the first player to press "Enter" to roll the dice. The dice is rolled, and since the player starts at the Hall, they are asked to "Press 1" to get to corridor. Once you Press 1, either the turn ends since the dice only rolled 1, or the turn continues and the player is asked where they would like to go. The output looks like this:
You are currently in Corridor
1: Hall. 
2: Kitchen. 
3: Bedroom. 
4: Ballroom. 
5: Bathroom. 
6: Dining. 
7: Backyard. 
8: Frontyard. 
9: Storage. 
You are in Corridor! You have the following rooms to go to! Enter the respective number for the room you need to go to!

From here, the player can select any option (enter the number left of the room you want to go to). If you go back to the Hall, you get this output:
Press 1 to make a suggestion, or Press 2 to make an accusation.

Regardless of the option, the cards the player has is flashed to the screen and the player is asked to pick which character did the crime (In the case of the suggestion, who they think "could have" done it). 
0: Miss Scarlett. 
1: Colonel Mustard. 
2: Mrs. White. 
3: Reverend Green. 
4: Mrs. Peacock. 
5: Professor Plum. 
Pick a number to guess which character you think is the murderer!

After this, the player is asked the weapon used for the crime.
0: Candlestick. 
1: Dagger. 
2: Lead Pipe. 
3: Revolver. 
4: Rope. 
5: Wrench. 
Select the weapon with which the murder took place. Enter a number from the give range of options!

If the player decided to make a suggestion, the turn ends here and the output shows this (Example: I suggested that Colonel Mustard might have used a Dagger, and I was in the Hall)
Player 0 suggests it was Colonel Mustard, who did it with Dagger, in Hall 
Player [1], who is, Colonel Mustard has been moved to Hall

If I decided to make an accusation, the turn will continue from the point I answered which weapon could have been used
0: Hall. 
1: Kitchen. 
2: Bedroom. 
3: Ballroom. 
4: Bathroom. 
5: Dining. 
6: Backyard. 
7: Frontyard. 
8: Storage. 
Select the location where the murder took place!

Once you type an option, either you get an indication that the answer is correct, or you got the answer wrong and are disqualified. This is what it looks like if I accused Mrs. Peacock did the crim with a Rope in the Backyard.

Player 0 has guessed the answer correctly! Mrs. Peacock, Rope, Backyard. The game has ended!

If my answer was incorrect, this is what I would see.
Player 0 guessed incorrectly, and is disqualified for the game!

My guess is not shown to anyone if I got it wrong, like the game states. And I cannot have any turns as the game goes till it ends.

The Accusation is only available if I am in the Hall. If I enter any other room from Corridor, I would only see this:
Press 1 to make a suggestion.

And then I will have to suggest the character name and weapon, and the character I suggested will be shifted to the room I am in.

As said before, there are only 2 secret passages:
    - Between Backyard and Frontyard
    - Between Bedroom and Storage

Here is how it looks like if you start your turn in the Bedroom.
Press 1 to go to Corridor. Press 2 for Secret Passage to Storage.

If the player decides to go to Storage, regardless of how much dice rolls they have left, the turn ends. But if they decide to go to the Corridor, the turn continues or ends depends on how much dice rolls they have.

Similar cases if you start your turn in Storage. And similar for Backyard <- -> Frontyard.

## IMPORTANT TIP: Always give option numbers based on what option numbers are given. If you give the wrong option number, you are asked again and again until you give the right option range. If you accidentally press Enter when the input expected is not Enter, the program ends. So take it slow as you play along.

## GAME HINT: Every card the players have is not part of the final answer. If a certain player makes a suggestion and the next turn, no new cards are added, then the player unknowingly suggested the right answer. Of course the program cannot detect this, but you could as you try to run it if you just want to have fun.

