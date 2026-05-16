# A simple text-based RPG battle game where the player and an enemy take turns attacking each other until one of them runs out of health.
import random as r  # importing random module to allow the enemy to choose a random move each turn


def check_game_over(
    player_health, enemy_health
):  # function to check if the game is over based on the health of the player and the enemy
    if player_health <= 0 and enemy_health <= 0:
        print("It's a tie!")
        return False
    elif player_health <= 0 and enemy_health > 0:
        print("You lose!")
        return False
    elif enemy_health <= 0 and player_health > 0:
        print("You win!")
        return False
    else:
        return True


def report(
    player_health, enemy_health
):  # function to report the current health of the player and the enemy after each turn
    print(f"Player Health: {player_health}")
    print(f"Enemy Health: {enemy_health}")


def main():  # main function to run the game loop and handle the player's and enemy's turns
    player_health = 100
    enemy_health = 100

    moves = {  # dictionary to store the different moves and their effects on the player's and enemy's health
        "normal": (0, -20),
        "special": (5, -10),
        "heal": (15, 0),
        "reckless": (-15, -30),
    }

    moves_list = list(moves.keys())
    print("Welcome to the RPG battle!\n")
    print(
        "type 'quit' at any time to exit the game. \n To play again restart the program."
    )
    current_turn = 1

    running = True
    while running:
        # player's turn
        if current_turn == 1:
            print("\nPlayer turn!")

            valid_input = False
            while valid_input == False:
                player_input = input(
                    "Choose your move (normal, special, heal, reckless): \n"
                )
                valid_input = (
                    player_input.lower() in moves_list or player_input.lower() == "quit"
                )
                if not valid_input:
                    print("Invalid move. Please choose again.")
            if player_input.lower() == "quit":
                print("Thanks for playing!")
                running = False
                break

            selected_move = moves[
                player_input.lower()
            ]  # get the effects of the selected move from the moves dictionary
            print(f"You used {player_input}!")
            player_health += selected_move[0]
            enemy_health += selected_move[1]
            report(player_health, enemy_health)
            running = check_game_over(player_health, enemy_health)

        # enemy's turn
        elif current_turn == -1:
            print("\nEnemy turn!")
            enemy_input = r.randint(0, 3)
            selected_move = moves[moves_list[enemy_input]]
            print(f"Enemy used {moves_list[enemy_input]}!")
            player_health += selected_move[1]
            enemy_health += selected_move[0]
            report(player_health, enemy_health)
            running = check_game_over(player_health, enemy_health)

        current_turn *= -1  # switch turns between the player and the enemy


main()
