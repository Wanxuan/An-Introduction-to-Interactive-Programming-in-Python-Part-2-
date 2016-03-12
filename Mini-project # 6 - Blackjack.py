# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
scored = False
outcome = ""
score = 0
BET_AMOUNT = 1

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []

    def __str__(self):
        ans = ""
        for i in range(len(self.card_list)):
            ans += str(self.card_list[i])+" "
        
        return "Now your hand card are: "+ans 	# return a string representation of a hand

    def add_card(self, card):
        self.card_list.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        card_sum = 0
        hasAce = False
        for card in	self.card_list:
            card_sum += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                hasAce = True
        if hasAce and card_sum <12:
            card_sum += 10
        return card_sum
   
    def draw(self, canvas, pos):
            # draw a hand on the canvas, use the draw method for cards  
        for card in range(0, len(self.card_list)):
            self.card_list[card].draw(canvas, [pos[0] + card * CARD_SIZE[0]*1.1, pos[1]])
            
    
# define deck class 
class Deck:
    def __init__(self):
            # create a Deck object
        self.deck_cards = [Card(i, j) for i in SUITS for j in RANKS]
                
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_cards)    # use random.shuffle()

    def deal_card(self):
        return self.deck_cards.pop()
            # deal a card object from the deck
    
    def __str__(self):
        deck_item = ""
        for i in self.deck_cards:
            deck_item += str(i)+" "
        return "Deck contains "+deck_item	# return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play, message, score
    global dealer, player, deck
    
    if in_play == True: score -= 1
        
    dealer = Hand()
    player = Hand()
    deck = Deck()
    deck.shuffle()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    outcome = "Hit or stand?"
    in_play = True
    


def hit():
    global in_play, player, message, outcome, score 
    # if the hand is in play, hit the player
    if in_play:
        if player.get_value() < 22:
            player.add_card(deck.deal_card())
            # if busted, assign a message to outcome, update in_play and score
            if player.get_value() > 21:
                outcome = "You've busted! New deal?"
                score -= BET_AMOUNT
                in_play = False
                
        
        
def stand():
    global in_play, player, dealer, outcome, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while (dealer.get_value() < 17):
                dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            outcome = "Dealer has busted! New deal?"
            in_play = False
            score += BET_AMOUNT
        elif dealer.get_value() > player.get_value():
            outcome = "Dealer wins! New deal?"
            in_play = False
            score -= BET_AMOUNT
        elif dealer.get_value() == player.get_value():
            outcome = "Tie. Dealer wins! New deal?"
            in_play = False
            score -= BET_AMOUNT
        else:
            outcome = "You win! New deal?"
            in_play = False
            score += BET_AMOUNT

# draw handler    
def draw(canvas):
    
#    card = Card("S", "A")
#    card.draw(canvas, [300, 300])
    global in_play, score
    canvas.draw_text("Blackjack", (200, 60), 40, 'Black', 'monospace')
    player.draw(canvas,[35,400])
    dealer.draw(canvas,[35,100])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (35+CARD_BACK_CENTER[0], 100+CARD_BACK_CENTER[1]), CARD_BACK_SIZE)
    canvas.draw_text(outcome, (35, 540), 20, 'Black', 'monospace')
    canvas.draw_text("Score: "+str(score), (35, 575), 20, 'Black', 'monospace')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
