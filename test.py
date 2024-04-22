import unittest
from main import Player, Dealer, Card, Hand, Deck

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Test Player", 100)
        self.deck = Deck()
        self.deck.shuffle()
        self.player.hand = Hand()

    def test_hit(self):
        initial_hand_size = len(self.player.hand.cards)
        self.player.hit(Card("Hearts", "2"))
        self.assertEqual(len(self.player.hand.cards), initial_hand_size + 1)

    def test_stand(self):
        initial_hand_size = len(self.player.hand.cards)
        self.player.stand()
        self.assertEqual(len(self.player.hand.cards), initial_hand_size)

    def test_double_down(self):
        initial_hand_size = len(self.player.hand.cards)
        initial_balance = self.player.balance
        self.player.double_down(Card("Hearts", "3"))
        self.assertEqual(len(self.player.hand.cards), initial_hand_size + 1)
        self.assertEqual(self.player.balance, initial_balance - self.player.bet)
    
    def test_split(self):
        self.player.hand.add_card(Card("Hearts", "2"))
        self.player.hand.add_card(Card("Diamonds", "2"))
        initial_hand_size = len(self.player.hand.cards)
        initial_balance = self.player.balance
        self.player.split(self.deck)
        self.assertEqual(len(self.player.hand), 2)
        for hand in self.player.hand:
            self.assertEqual(len(hand.cards), 1)
        self.assertEqual(self.player.balance, initial_balance - self.player.bet)


    def test_surrender(self):
        initial_balance = self.player.balance
        self.player.surrender()
        self.assertEqual(self.player.balance, initial_balance - self.player.bet / 2)
        self.assertEqual(len(self.player.hand.cards), 0)
    
    def test_double_down(self):
        initial_hand_size = len(self.player.hand.cards)
        initial_balance = self.player.balance
        self.player.double_down(Card("Hearts", "3"))
        self.assertEqual(len(self.player.hand.cards), initial_hand_size + 1)
        self.assertEqual(self.player.balance, initial_balance - self.player.bet)

class TestDealer(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Dealer(self.deck)
        # Setup for Blackjack hand
        self.dealer.hand.add_card(Card("Hearts", "Ace"))
        self.dealer.hand.add_card(Card("Diamonds", "King"))
    
    def test_player_wins(self):
        # Assuming player has a hand value higher than dealer
        self.dealer.hand.add_card(Card("Clubs", "9"))    # Dealer's hand value: 19
        player = Player("Test Player", 100)
        player.hand.add_card(Card("Hearts", "10"))      # Player's hand value: 20
        initial_balance = player.balance
        self.dealer.settle_bets(player)
        self.assertEqual(player.balance, initial_balance + player.bet)

    def test_player_blackjack(self):
        # Assuming player has a Blackjack
        player = Player("Test Player", 100)
        player.hand.add_card(Card("Hearts", "Ace"))
        player.hand.add_card(Card("Clubs", "King"))
        initial_balance = player.balance
        self.dealer.settle_bets(player)
        self.assertEqual(player.balance, initial_balance + player.bet * 1.5)

    def test_push(self):
        # Assuming player and dealer have the same hand value
        player = Player("Test Player", 100)
        player.hand.add_card(Card("Hearts", "10"))
        self.dealer.hand.add_card(Card("Clubs", "10"))
        initial_balance = player.balance
        self.dealer.settle_bets(player)
        self.assertEqual(player.balance, initial_balance)
    
    def test_dealer_wins(self):
        # Assuming dealer has a hand value higher than player
        player = Player("Test Player", 100)
        player.hand.add_card(Card("Hearts", "9"))      # Player's hand value: 19
        self.dealer.hand.add_card(Card("Clubs", "10")) # Dealer's hand value: 20
        initial_balance = player.balance
        self.dealer.settle_bets(player)
        self.assertEqual(player.balance, initial_balance - player.bet)

    def test_hit(self):
        initial_hand_size = len(self.dealer.hand.cards)
        self.dealer.hit(self.deck.draw())
        self.assertEqual(len(self.dealer.hand.cards), initial_hand_size + 1)

    def test_stand(self):
        initial_hand_size = len(self.dealer.hand.cards)
        self.dealer.stand()
        self.assertEqual(len(self.dealer.hand.cards), initial_hand_size)

    def test_has_blackjack(self):
        self.assertTrue(self.dealer.has_blackjack())

    def test_reveal_downcard(self):
        downcard = self.dealer.reveal_downcard()
        self.assertEqual(str(downcard), "King of Diamonds")

    def test_settle_insurance(self):
        # Assuming dealer has a Blackjack
        players = [Player("Player 1", 100), Player("Player 2", 100)]
        for player in players:
            player.bet = 10  # Assume all players took insurance with a bet of 10
        initial_balances = [player.balance for player in players]
        self.dealer.settle_insurance(players)
        for i, player in enumerate(players):
            expected_balance = initial_balances[i] + player.bet * 2
            self.assertEqual(player.balance, expected_balance)
    
    


if __name__ == '__main__':
    unittest.main()
