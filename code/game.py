from yatzy import Yatzy
import time
import sys

class YatzyGame:
    def __init__(self):
        self.game = Yatzy()
        self.scorecard = {}
        self.category_names = {
            'ones': "Ones",
            'twos': "Twos",
            'threes': "Threes",
            'fours': "Fours",
            'fives': "Fives",
            'sixes': "Sixes",
            'one_pair': "One Pair",
            'two_pairs': "Two Pairs",
            'three_alike': "Three of a Kind",
            'four_alike': "Four of a Kind",
            'small_straight': "Small Straight",
            'large_straight': "Large Straight",
            'full_house': "Full House",
            'chance': "Chance",
            'yatzy': "Yatzy"
        }
        
    def show_dice(self):
        print("\nCurrent Dice:")
        for i in range(5):
            die = self.game.dice[i]
            lock_status = " (Locked)" if self.game.locked[i] else ""
            print(f"    Die {i+1}: {die}{lock_status}")
            
    def show_scorecard(self):
        print("\nYour Scorecard:")
        print("-" * 30)
        for category, score in self.scorecard.items():
            print(f"  {self.category_names.get(category, category):<20}: {score:>3}")
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
        categories = [m for m in dir(self.game) 
                     if not m.startswith('_') and callable(getattr(self.game, m))
                     and m not in ['roll', 'lock_die', 'unlock_die', 'reset_turn']]
        
        available = [cat for cat in categories if cat not in self.scorecard]
        
        for i, cat in enumerate(available, 1):
            print(f"  {i:>2}. {self.category_names.get(cat, cat)}")
            
        return available
        
    def handle_command(self, cmd):
        try:
            if cmd == "roll":
                if self.game.roll_count >= 3:
                    print("You've already rolled 3 times this turn!")
                    return False
                self.roll_animation()
                self.game.roll()
                self.show_dice()
                
            elif cmd.startswith("lock"):
                die = int(cmd.split()[1]) - 1
                if not 0 <= die < 5:
                    raise ValueError
                self.game.lock_die(die)
                self.show_dice()
                
            elif cmd.startswith("unlock"):
                die = int(cmd.split()[1]) - 1
                if not 0 <= die < 5:
                    raise ValueError
                self.game.unlock_die(die)
                self.show_dice()
                
            elif cmd == "score":
                return True
                
            elif cmd == "quit":
                print("\nThanks for playing! Final scores:")
                self.show_scorecard()
                sys.exit()
                
            else:
                print("Invalid command. Try 'help' for options.")
                
        except (ValueError, IndexError):
            print("Invalid command. Usage examples:")
            print("  lock 3  - to lock die #3")
            print("  unlock 2 - to unlock die #2")
            
        return False
        
    def score_turn(self):
        self.show_dice()
        available = self.show_available_categories()
        
        while True:
            choice = input("\nChoose category number (or 'back' to continue playing): ").lower()
            
            if choice == "back":
                return False
            if choice == "quit":
                print("\nThanks for playing! Final scores:")
                self.show_scorecard()
                sys.exit()
                
            try:
                cat = available[int(choice)-1]
                score = getattr(self.game, cat)()
                self.scorecard[cat] = score
                print(f"\nScored {score} points for {self.category_names.get(cat, cat)}!")
                return True
                
            except (ValueError, IndexError):
                print("Invalid choice. Please enter a number from the list.")
                
    def take_turn(self):
        self.game.reset_turn()
        print("\n=== New Turn === (Rolls left: 3)")
        
        while True:
            self.show_dice()
            cmd = input("\nCommand (roll/lock/unlock/score/quit/help): ").lower()
            
            if cmd == "help":
                print("\nAvailable Commands:")
                print("  roll         - Roll unlocked dice")
                print("  lock <1-5>   - Lock a die (e.g., 'lock 2')")
                print("  unlock <1-5> - Unlock a die (e.g., 'unlock 3')")
                print("  score        - Score your current dice")
                print("  quit         - End the game")
                continue
                
            if self.handle_command(cmd):
                if self.score_turn():
                    break

def main():
    print("""
    Welcome to Yatzy!
    The dice game where you score points by rolling different combinations.
    
    Basic Commands:
    - roll         : Roll unlocked dice
    - lock <1-5>   : Lock a die (e.g., 'lock 2')
    - unlock <1-5> : Unlock a die (e.g., 'unlock 3')
    - score        : End turn and choose category
    - quit         : Exit game
    - help         : Show this help message
    
    You'll have 3 rolls per turn. After rolling, you can lock dice 
    you want to keep and re-roll the others.
    """)
    
    game = YatzyGame()
    while len(game.scorecard) < 15:
        game.take_turn()
        game.show_scorecard()
        
    print("\nGame Over! You've played all categories!")
    print(f"Final Score: {sum(game.scorecard.values())} points")

if __name__ == "__main__":
    main()