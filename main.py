import random 

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    def __init__(self):
        self.cards = []
        for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]:
            for rank in range(2, 11):
                self.cards.append(Card(suit, str(rank)))
            for rank in ["Jack", "Queen", "King", "Ace"]:
                self.cards.append(Card(suit, rank))
    
    def __str__(self):
        deck_comp = ""
        for card in self.cards:
            deck_comp += "\n" + card.__str__()
        return f"The deck has: {deck_comp}"

    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self):
        if not self.cards:
            print("Cannot draw from an empty deck")
            self.shuffle()
            return self.draw()  # Draw again after shuffling
        return self.cards.pop()
  
class Hand:
    def __init__(self):
        self.cards = []
    
    def __str__(self) -> str:
        hand_str = "Cards:\n"
        for card in self.cards:
            hand_str += str(card) + "\n"
        return hand_str
    
    def add_card(self, card):
        self.cards.append(card)
    
    def get_value(self):
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank in ["Jack", "Queen", "King"]:
                value += 10
            elif card.rank == "Ace":
                num_aces += 1
            else:
                value += int(card.rank)
        for _ in range(num_aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1     
        return value
    
class Player:
    def __init__(self, name, balance):
        self.name = name 
        self.balance = balance
        self.hand = Hand()
        self.bet = 0
    
    def can_split_aces(self):
        return len(self.hand.cards) == 2 and self.hand.cards[0].rank == 'Ace'

    def split_aces(self, deck):
        if not self.can_split_aces():
            print("You cannot split Aces in this situation.")
            return False
        if self.balance < self.bet:
            print("Insufficient balance to place the additional bet for splitting.")
            return False
        new_hands = []
    
        # Iterate through the cards in the hand
        for card in self.hand.cards:
            # Check if the card is an Ace
            if card.rank == 'Ace':
                # Create a new hand with the Ace
                new_hand = Hand()
                new_hand.add_card(card)
                # Add the new hand to the list of new hands
                new_hands.append(new_hand)
            else:
                # Create a new hand with the non-Ace card
                new_hand = Hand()
                new_hand.add_card(card)
                # Add the new hand to the list of new hands
                new_hands.append(new_hand)
            
        self.hand = new_hands
        self.balance -= self.bet  # Place the additional bet for splitting
        return True

        
        
        #split_card = self.hand.cards.pop()  # Remove one Ace from the hand
        #new_hand = Hand()
        #new_hand.add_card(split_card)  # Create a new hand with the split Ace
        #self.hand = new_hand
        #self.balance -= self.bet  # Place the additional bet for splitting
        #return True
        
    def hit(self, card):
        self.hand.add_card(card)
    
    def clear_hand(self):
        self.hand = Hand()
    
    def stand(self):
        print(f"{self.name} is standing")

    def double_down(self, card):
        if self.balance < self.bet * 2:
            print("Insufficient balance to double down.")
            return False
        self.hit(card)
        self.balance -= self.bet
        self.bet *= 2
        return True
    
    def double_down_after_split(self, card):
        if len(self.hand.cards) != 2:
            print("You can only double down after splitting with exactly two cards in your hand.")
            return False
        self.double_down(card)
    
    def split(self, deck):
        if len(self.hand.cards) != 2:
            print("You can only split with exactly two cards in your hand.")
            return
        if self.hand.cards[0].rank != self.hand.cards[1].rank:
            print("You can only split if the two cards in your hand are the same rank.")
            return
        if self.balance < self.bet:
            print("Insufficient balance to place the additional bet for splitting.")
            return
        # Create two new hands
        new_hands = [Hand(), Hand()]
        # Distribute cards from the original hand to the new hands
        for card in self.hand.cards:
            new_hands[self.hand.cards.index(card) % 2].add_card(card)
        self.hand = new_hands
        self.balance -= self.bet  # Place the additional bet for splitting


        


    def surrender(self):
        print(f"{self.name} is surrenders")
        self.balance -= self.bet / 2
        self.clear_hand()  # Clear the player's hand after surrendering
    
class Dealer(Player):
    def __init__(self, deck):
        super().__init__('Dealer', float('inf'))
        self.deck = deck
    
    def game_over(self):
        return len(self.deck.cards) == 0

    def check_insurance(self, players):
        if self.hand.cards[0].rank == 'Ace':
            for player in players:
                if player.take_insurance():
                    player.balance -= player.bet / 2

    def reveal_downcard(self):
        # Reveal the dealer's face-down card
        return self.hand.cards[1]

    def has_blackjack(self):
        return self.hand.get_value() == 21 and len(self.hand.cards) == 2

    def settle_insurance(self, players):
        if self.has_blackjack():
            print("Dealer has Blackjack!")
            for player in players:
                if player.balance >= player.bet:
                    player.balance += player.bet * 2  # Insurance bet pays 2:1
                else:
                    print(f"{player.name} doesn't have enough balance to receive the insurance payout.")
    
    def deal_initial_cards(self, players):
        for _ in range(2):
            for player in players:
                player.hand.add_card(self.deck.draw())
        self.hand.add_card(self.deck.draw())  # Deal one card face up
        self.hand.add_card(self.deck.draw())  # Deal one card face down

    def play_turn(self):
        while self.hand.get_value() < 17:
            self.hit(self.deck.draw())

    def reveal_first_card(self):
        if self.hand.cards:  # Check if the dealer has at least one card
            return self.hand.cards[0]
        else:
            return "No card revealed"

    def settle_bets(self, players):
        dealer_value = self.hand.get_value()
        if isinstance(players, Player):
            players = [players]  # Convert single player to a list

        for player in players:
            player_value = player.hand.get_value()
            if player_value > 21:  # Player busts
                player.balance -= player.bet
            elif dealer_value > 21:  # Dealer busts
                player.balance += player.bet
            elif dealer_value > player_value:  # Dealer wins
                player.balance -= player.bet
            elif dealer_value < player_value:  # Player wins
                player.balance += player.bet
            # Handle tie scenario (push)
            elif dealer_value == player_value:  
                print("It's a tie!")
                # Player neither wins nor loses money
            else:
                # This shouldn't happen under normal circumstances
                print("An unexpected scenario occurred.")


    def clear_hand(self):
        self.hand = Hand()

class Statistics:
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.games = 0
        self.draws = 0
        self.total_bet = 0
       
    
    def update_stats(self, winner):
        self.games += 1
        if winner == "Player":
            self.wins += 1
        elif winner == "Dealer":
            self.losses += 1
        else:
            self.draws += 1
    
    def print_stats(self, winner):
        print(f"{winner} wins: {self.wins}, losses: {self.losses}, draws")

def determine_winner(players, dealer):
        dealer_value = dealer.hand.get_value()
        dealer_blackjack = dealer.has_blackjack()
        winner = None

        for player in players:
            player_value = player.hand.get_value()
            player_blackjack = player_value == 21 and len(player.hand.cards) == 2

            if player_blackjack and not dealer_blackjack:  # Player has Blackjack, dealer does not
                winner = player
            elif not player_blackjack and dealer_blackjack:  # Dealer has Blackjack, player does not
                return dealer
            elif player_value > 21:  # Player busts
                return dealer
            elif dealer_value > 21:  # Dealer busts
                return player
            elif player_value > dealer_value:  # Player wins
                winner = player
            elif player_value < dealer_value:  # Dealer wins
                winner = dealer

        return winner


def player_turn(player, dealer):
    print("\n-------------------------------------------------------------")
    print(f"\n{player.name}'s Turn")
    print("-------------------------------------------------------------")

    if player.balance <= 0:
        print(f"{player.name} has run out of credits and cannot play further.")
        return

    print(f"Dealer's Visible Card: {dealer.reveal_first_card()}")
    print(f"{player.name}'s Hand: {player.hand}")
    print(f"{player.name}'s Balance: {player.balance}")

    bet = 0
    while True:
        try:
            bet = int(input(f"Place your bet (current balance: {player.balance}): "))
            if bet <= 0:
                print("Invalid bet amount. Please enter a positive integer.")
            elif bet > player.balance:
                print("Insufficient balance. Please enter a bet amount within your balance.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    player.bet = bet
    player.balance -= bet  

    while True:
        action = input("Choose your action (hit (H), stand (S), double down (D), split (Sp), surrender(Su)): ").upper()
        if action in ["H", "S", "D", "SP", "SU"] or action.lower() in ["h", "s", "d", "sp", "su"]:
            break
        else:
            print("Invalid input. Please try again with one of the suggested inputs.")

    if action == "H":
        player.hit(dealer.deck.draw())
    elif action == "S":
        player.stand()
    elif action == "D":
        if player.double_down(dealer.deck.draw()):
            player.balance -= player.bet  
    elif action == "Sp":
        player.split(dealer.deck)
    elif action == "Su":
        player.surrender()
        print(f"{player.name} surrenders")
        player.balance += player.bet / 2  

    print(f"{player.name}'s Hand after their turn: {player.hand}")

    if player.hand.get_value() == 21:
        print("Blackjack!")
    elif player.hand.get_value() > 21:
        print("Busted!") 

    print(f"{player.name}'s Balance after their turn: {player.balance}")


def dealer_turn(dealer):
    print("\n-------------------------------------------------------------")
    print(f"Dealer's Turn")
    print("-------------------------------------------------------------")
    print(f"Dealer's current hand: {[str(card) for card in dealer.hand.cards]}")
    dealer.play_turn()

    print(f"Dealer's hand after their turn: {[str(card) for card in dealer.hand.cards]}")
    


def main():
    print("\n-------------------------------------------------------------")
    print("\n-------------------------------------------------------------")
    print("                   ♠♣♥♦ WELCOME TO BLACKJACK! ♠♣♥♦             ")
    print("                        Let the games begin                    ")
    print("\n-------------------------------------------------------------")
    print("\n-------------------------------------------------------------")

    player1 = Player("Player 1", 100)
    player2 = Player("Player 2", 100)
    player3 = Player("Player 3", 100)

    dealer = Dealer(Deck())

    dealer.deck.shuffle()

    players = [player1, player2, player3]

    dealer.deal_initial_cards(players)

    game_stats = Statistics()  # Initialize game statistics

    while True:
        active_players = [player for player in players if player.balance > 0]

        if not active_players:
            print("All players have run out of credits. Game over!")
            break

        for player in active_players:
            player_turn(player, dealer)

        dealer_turn(dealer)

        dealer.settle_bets(active_players)

        for player in players:
            if player.balance <= 0:
                print(f"{player.name} has run out of credits and lost the game. Game over!")
                players.remove(player)

        if not players:
            print("All players have run out of credits. Game over!")
            break

        # Determine the winner
        winner = determine_winner(active_players, dealer)


        game_stats.update_stats(winner)

        # Print statistics for the winner only
        #game_stats.print_stats(winner)

        # Clear hands for the next round
        for player in active_players:
            player.clear_hand()
        dealer.clear_hand()

        play_again = input("\nDo you want to play again? Press Y. If not, press any key to exit").upper()
        if play_again != "Y":50
        break

        print("\n-------------------------------------------------------------")
        print("\n-------------------------------------------------------------")
        print("                   ♠♣♥♦ WELCOME TO BLACKJACK! ♠♣♥♦             ")
        print("                        Let the games begin                    ")
        print("\n-------------------------------------------------------------")
        print("\n-------------------------------------------------------------")

        player1.clear_hand()
        player2.clear_hand()
        player3.clear_hand()
        dealer.clear_hand()

    

if __name__ == '__main__':
    main()