import random
import time
import argparse


class Die:
    def __init__(self):
        pass  # Removed the seed for true randomness

    def roll(self):
        return random.randint(1, 6)


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_score(self, points):
        self.score += points


class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def decide_action(self, turn_total):
        # Computer holds at the lesser of 25 and 100 - current score
        if turn_total >= min(25, 100 - self.score):
            return 'h'
        else:
            return 'r'


class PlayerFactory:
    def create_player(player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError(f"Unknown player type: {player_type}")


class Game:
    def __init__(self, player1_type, player2_type):
        self.players = [
            PlayerFactory.create_player(player1_type, "Player 1"),
            PlayerFactory.create_player(player2_type, "Player 2")
        ]
        self.current_player_index = 0
        self.target_score = 100
        self.die = Die()  # Create a single Die instance

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % 2

    def play(self):
        while True:
            if self.play_turn():
                break
            self.switch_player()

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        turn_total = 0

        while True:
            print(f"{current_player.name}'s turn. Current score: {current_player.score}, Turn total: {turn_total}")
            if isinstance(current_player, ComputerPlayer):
                action = current_player.decide_action(turn_total)
                print(f"{current_player.name} decides to '{action}'")
            else:
                action = input("Enter 'r' to roll or 'h' to hold: ")

            if action == 'r':
                rolled_value = self.die.roll()  # Use the same Die instance
                print(f"You rolled a {rolled_value}")

                if rolled_value == 1:
                    print("You rolled a 1! Turn ends with no points.")
                    break
                else:
                    turn_total += rolled_value
            elif action == 'h':
                current_player.add_score(turn_total)
                break
            else:
                print("Invalid input. Please enter 'r' to roll or 'h' to hold.")

        if current_player.score >= self.target_score:
            print(f"{current_player.name} wins with a score of {current_player.score}!")
            return True  # Game over
        return False  # Game continues


class TimedGameProxy:
    def __init__(self, game):
        self.game = game
        self.start_time = time.time()

    def play(self):
        while True:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 60:  # 1 minute limit
                print("Time is up!")
                self.determine_winner()
                break
            if self.game.play_turn():
                break
            self.game.switch_player()

    def determine_winner(self):
        if self.game.players[0].score > self.game.players[1].score:
            print(f"{self.game.players[0].name} wins with {self.game.players[0].score} points!")
        elif self.game.players[0].score < self.game.players[1].score:
            print(f"{self.game.players[1].name} wins with {self.game.players[1].score} points!")
        else:
            print("It's a tie!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play the game of Pig.')
    parser.add_argument('--player1', choices=['human', 'computer'], required=True, help='Type of player 1')
    parser.add_argument('--player2', choices=['human', 'computer'], required=True, help='Type of player 2')
    parser.add_argument('--timed', action='store_true', help='Play a timed version of the game')
    args = parser.parse_args()

    game = Game(args.player1, args.player2)

    if args.timed:
        timed_game = TimedGameProxy(game)
        timed_game.play()
    else:
        game.play()
    pass