import random as rand

class Card:
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def __str__(self):
        return self.name.capitalize()

class AceCard(Card):
    def __init__(self):
        super().__init__("Ace", [1, 11])

    def best_value(self, current_total):
        return 11 if current_total + 11 <= 21 else 1

class FaceCard(Card):
    def __init__(self, name):
        if name.lower() not in ["jack", "queen", "king"]:
            raise ValueError("Invalid face card")
        super().__init__(name.capitalize(), [10])

class Deck:
    def __init__(self):
        self.cards = self.create_deck()
        rand.shuffle(self.cards)

    def create_deck(self):
        cards = []

        # Aces
        for _ in range(4):
            cards.append(AceCard())

        # Numbered cards
        for num in range(2, 11):
            for _ in range(4):
                cards.append(Card(str(num), [num]))

        # Face cards
        for face in ["Jack", "Queen", "King"]:
            for _ in range(4):
                cards.append(FaceCard(face))

        return cards

    def deal(self):
        if not self.cards:
            self.cards = self.create_deck()
            rand.shuffle(self.cards)
        return self.cards.pop()

def calculate_hand_total(hand):
    total = 0
    aces = []

    for card in hand:
        if isinstance(card, AceCard):
            aces.append(card)
        else:
            total += card.values[0]

    for ace in aces:
        total += ace.best_value(total)

    return total

def print_hand(hand, owner="Player"):
    print(f"{owner}'s hand: ", ", ".join(str(card) for card in hand))

def play():
    rand.seed()
    balance = 100
    print("🎲 Welcome to Blackjack!")

    while balance > 0:
        print(f"\n💰 Current Balance: ${balance}")
        try:
            bet = int(input("Enter your bet: $"))
            if bet <= 0 or bet > balance:
                print("Invalid bet amount.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        deck = Deck()
        player_hand = [deck.deal(), deck.deal()]
        dealer_hand = [deck.deal(), deck.deal()]

        print_hand(player_hand)
        print("Dealer shows:", dealer_hand[0])

        # Player Turn
        while True:
            total = calculate_hand_total(player_hand)
            print("Your Total:", total)

            if total > 21:
                print("❌ You busted!")
                balance -= bet
                break

            choice = input("Hit or Stand? ").strip().lower()
            if choice == "hit":
                player_hand.append(deck.deal())
                print_hand(player_hand)
            elif choice == "stand":
                break
            else:
                print("Please enter 'hit' or 'stand'.")

        player_total = calculate_hand_total(player_hand)
        if player_total > 21:
            print("Dealer Wins!")
        else:
            print_hand(dealer_hand, "Dealer")
            dealer_total = calculate_hand_total(dealer_hand)
            while dealer_total < 17:
                print("Dealer Hits.")
                dealer_hand.append(deck.deal())
                dealer_total = calculate_hand_total(dealer_hand)
                print_hand(dealer_hand, "Dealer")

            print("Dealer's Total:", dealer_total)

            if dealer_total > 21:
                print("✅ Dealer busted! You win!")
                balance += bet
            elif dealer_total > player_total:
                print("❌ Dealer Wins.")
                balance -= bet
            elif dealer_total < player_total:
                print("✅ You Win!")
                balance += bet
            else:
                print("🤝 It's a Tie!")

        again = input("\nPlay another round? (yes/no): ").strip().lower()
        if again != 'yes':
            break

    print(f"\nGame Over. Final balance: ${balance}")

play()
