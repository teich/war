import random
import sys
from collections import Counter

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

# Card values and suits
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['♥', '♦', '♣', '♠']

def create_deck():
    return [(value, suit) for value in values for suit in suits]

def parse_card(card_str):
    value, suit = card_str[:-1], card_str[-1]
    if value not in values or suit not in '♥♦♣♠HDCS':
        raise ValueError(f"Invalid card: {card_str}")
    suit = {'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠'}.get(suit, suit)
    return (value, suit)

def deal_custom_cards(deck, player1_cards):
    player1 = [parse_card(card.strip()) for card in player1_cards.split(',')]
    player2 = [card for card in deck if card not in player1]
    return player1, player2

def compare_cards(card1, card2):
    return values.index(card1[0]) - values.index(card2[0])

def play_war(player1_starting_cards=None):
    deck = create_deck()
    if player1_starting_cards:
        player1, player2 = deal_custom_cards(deck, player1_starting_cards)
    else:
        random.shuffle(deck)
        middle = len(deck) // 2
        player1, player2 = deck[:middle], deck[middle:]
    
    round_num = 0
    previous_states = set()
    
    while player1 and player2:
        round_num += 1
        
        if round_num > 10000:
            return "Draw (Round limit)"
        
        # Check for repeated state
        current_state = (tuple(sorted(player1)), tuple(sorted(player2)))
        if current_state in previous_states:
            return "Draw (Repeated state)"
        previous_states.add(current_state)
        
        card1 = player1.pop(0)
        card2 = player2.pop(0)
        
        war_pile = [card1, card2]
        
        while True:
            result = compare_cards(card1, card2)
            
            if result > 0:
                random.shuffle(war_pile)
                player1.extend(war_pile)
                break
            elif result < 0:
                random.shuffle(war_pile)
                player2.extend(war_pile)
                break
            else:
                # War situation
                if not player1 or not player2:
                    return "Draw (Empty deck before)"
                
                if len(player1) < 3 and len(player2) < 3:
                    # Both players don't have enough cards for war
                    return "Draw (Insufficient cards for war)"
                elif len(player1) < 3:
                    player2.extend(war_pile)
                    player2.extend(player1)
                    player1.clear()
                    break
                elif len(player2) < 3:
                    player1.extend(war_pile)
                    player1.extend(player2)
                    player2.clear()
                    break
                
                # Both players have enough cards for war
                war_pile.extend(player1[:3] + player2[:3])
                player1 = player1[3:]
                player2 = player2[3:]
                
                if not player1 or not player2:
                    # One player ran out of cards during war
                    return "Draw (Empty deck during)"
                
                card1 = player1.pop(0)
                card2 = player2.pop(0)
                war_pile.extend([card1, card2])
    
    if not player1 and not player2:
        return "Draw (Both empty)"
    return "Player 1" if player1 else "Player 2"
def print_fancy_results(results, total_games):
    print(f"\n{BOLD}{MAGENTA}╔═══════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{MAGENTA}║           War Game Simulation Results         ║{RESET}")
    print(f"{BOLD}{MAGENTA}╚═══════════════════════════════════════════════╝{RESET}\n")

    print(f"{CYAN}Total games played: {BOLD}{total_games}{RESET}\n")

    max_count = max(results.values())
    bar_width = 30

    for outcome, count in sorted(results.items(), key=lambda x: x[1], reverse=True):
        percentage = count / total_games * 100
        bar_length = int(count / max_count * bar_width)
        
        if "Player 1" in outcome:
            color = RED
        elif "Player 2" in outcome:
            color = BLUE
        else:
            color = YELLOW

        print(f"{color}{outcome:<25}{RESET} {BOLD}{count:5}{RESET} {percentage:6.2f}% {color}{'█' * bar_length}{RESET}")

    print(f"\n{GREEN}♠ ♥ ♦ ♣ Game Over ♣ ♦ ♥ ♠{RESET}")

def main(player1_cards, num_games):
    results = Counter()
    
    print(f"{BOLD}{CYAN}Shuffling cards and dealing hands...{RESET}")
    for i in range(num_games):
        if i % (num_games // 10) == 0 and i > 0:
            print(f"{YELLOW}Completed {i} games...{RESET}")
        winner = play_war(player1_cards)
        results[winner] += 1
    
    total_games = sum(results.values())
    print_fancy_results(results, total_games)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"{RED}Usage: python script.py <num_games> [player1_cards]{RESET}")
        print(f"{GREEN}Example with custom cards: python script.py 1000 'A♠,K♦,Q♥,J♣,10♠,9♦,8♥,7♣'{RESET}")
        print(f"{GREEN}Example with random deal: python script.py 1000{RESET}")
        sys.exit(1)
    
    num_games = int(sys.argv[1])
    player1_cards = sys.argv[2] if len(sys.argv) == 3 else None
    
    main(player1_cards, num_games)