from yatzy import Yatzy
import time
import sys

class YatzyGame:
    def __init__(self):
        self.game = Yatzy()
        self.scorecard = {}
        self.category_names = {
            'ones': "Ones", 'twos': "Twos", 'threes': "Threes",
            'fours': "Fours", 'fives': "Fives", 'sixes': "Sixes",
            'one_pair': "One Pair", 'two_pairs': "Two Pairs",
            'three_alike': "Three of a Kind", 'four_alike': "Four of a Kind",
            'small_straight': "Small Straight", 'large_straight': "Large Straight",
            'full_house': "Full House", 'chance': "Chance", 'yatzy': "Yatzy"
        }
        
    def show_dice(self):
        print("\nCurrent Dice:")
        for i in range(5):
            status = " (Locked)" if self.game.locked[i] else ""
            print(f"    Die {i+1}: {self.game.dice[i]}{status}")
            
    def show_scorecard(self):
        print("\nYour Scorecard:")
        print("-" * 30)
        for cat, score in self.scorecard.items():
            print(f"  {self.category_names.get(cat, cat):<20}: {score:>3}")
        print("-" * 30)
        print(f"  {'Total Score':<20}: {sum(self.scorecard.values()):>3}\n")
            
    def roll_animation(self):
        print("\nRolling dice", end="")
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.3)
        print("\n")
        
    def show_available_categories(self):
        print("\nAvailable Scoring Categories:")
        categories = [
            m for m in dir(self.game) 
            if not m.startswith('_') 
            and callable(getattr(self.game, m))
            and m not in ['roll', 'lock_die', 'unlock_die', 'reset_turn']
        ]
        available = [cat for cat in categories if cat not in self.scorecard]
        for i, cat in enumerate(available, 1):
            print(f"  {i:>2}. {self.category_names.get(cat, cat)}")
        return available
        
    def handle_command(self, cmd):
        try:
            if cmd == "roll":
                if self.game.roll_count >= 3:
                    print("Maximum 3 rolls per turn!")
                    return False
                self.roll_animation()
                self.game.roll()
                self.show_dice()
            elif cmd.startswith("lock"):
                die = int(cmd.split()[1]) - 1
                self.game.lock_die(die)
                self.show_dice()
            elif cmd.startswith("unlock"):
                die = int(cmd.split()[1]) - 1
                self.game.unlock_die(die)
                self.show_dice()
            elif cmd == "score":
                return True
            elif cmd == "quit":
                print("\nThanks for playing!")
                self.show_scorecard()
                sys.exit()
            else:
                print("Invalid command. Try 'help'")
        except (ValueError, IndexError):
            print("Invalid command. Examples:")
            print("  lock 3  - Lock die #3")
            print("  unlock 2 - Unlock die #2")
        return False
        
    def score_turn(self):
        self.show_dice()
        available = self.show_available_categories()
        while True:
            choice = input("\nChoose category (or 'back'): ").lower()
            if choice == "back":
                return False
            if choice == "quit":
                print("\nThanks for playing!")
                self.show_scorecard()
                sys.exit()
            try:
                cat = available[int(choice)-1]
                score = getattr(self.game, cat)()
                self.scorecard[cat] = score
                print(f"\nScored {score} for {self.category_names.get(cat, cat)}!")
                return True
            except (ValueError, IndexError):
                print("Invalid choice. Enter a number from the list.")
                
    def take_turn(self):
        self.game.reset_turn()
        print("\n=== New Turn === (Rolls left: 3)")
        while True:
            self.show_dice()
            cmd = input("\nCommand (roll/lock/unlock/score/quit/help): ").lower()
            if cmd == "help":
                print("\nCommands:")
                print("  roll         - Roll unlocked dice")
                print("  lock <1-5>   - Lock a die")
                print("  unlock <1-5> - Unlock a die")
                print("  score        - Score current dice")
                print("  quit         - End game")
                continue
            if self.handle_command(cmd):
                if self.score_turn():
                    break

def main():
    print("""
    Welcome to Yatzy!
    Commands:
    - roll         : Roll unlocked dice
    - lock <1-5>   : Lock a die
    - unlock <1-5> : Unlock a die
    - score        : Score dice
    - quit         : Exit game
    - help         : Show help
    """)
    game = YatzyGame()
    while len(game.scorecard) < 15:
        game.take_turn()
        game.show_scorecard()
    print("\nGame Over! Final Score:", sum(game.scorecard.values()))

if __name__ == "__main__":
    main()