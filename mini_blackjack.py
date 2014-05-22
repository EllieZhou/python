#Blackjack
#Xiaolan Zhou

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
instruction = "Hit or Stand?"
score = 0

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
        # create Hand object
        self.hand_list = []
    
    def __str__(self):
        # return a string representation of a hand
        str_hand = "Hand contains:"
        for i in range(len(self.hand_list)):
            str_hand += " "
            str_hand += str(self.hand_list[i])
        return str_hand
    
    def add_card(self, card):
        # add a card object to a hand
        self.hand_list.append(card)
    
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_ranks = []
        hand_value = 0
        for i in range(len(self.hand_list)):
            hand_ranks.append( self.hand_list[i].get_rank() )
            hand_value += VALUES[ self.hand_list[i].get_rank() ]
        
        if ('A' in hand_ranks) and (( hand_value + 10 ) <= 21) :
            hand_value += 10
        
        return hand_value
    
    
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        if len(self.hand_list) <= 5:
            for i in range(len(self.hand_list)):
                pos_i = ( pos[0]+ i*(CARD_SIZE[0] + CARD_CENTER[0]), pos[1])
                self.hand_list[i].draw(canvas, pos_i)
        else:
            for i in range(5):
                pos_i = ( pos[0]+ i*(CARD_SIZE[0] + CARD_CENTER[0]), pos[1])
                self.hand_list[i].draw(canvas, pos_i)


# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck_list = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_list.append( Card(suit , rank) )
    
    def shuffle(self):
        # shuffle the deck
        # use random.shuffle()
        random.shuffle( self.deck_list )
    
    def deal_card(self):
        # deal a card object from the deck
        card_dealed = self.deck_list[0]
        self.deck_list.remove(self.deck_list[0])
        return card_dealed
    
    def __str__(self):
        # return a string representing the deck
        str_deck = "Deck contains:"
        for i in range(len(self.deck_list)):
            str_deck += " " + str(self.deck_list[i])
        return str_deck


#define event handlers for buttons
def deal():
    global outcome, in_play, instruction, score
    #shuffle the deck (stored as a global variable)
    global deck_inplay
    if in_play == True:
        outcome = "You lose"
        instruction = "New deal?"
        in_play = False
        score -= 1
    else:
        outcome = ""
        instruction = " Hit or Stand?"
        in_play = True
        
        deck_inplay = Deck()
        deck_inplay.shuffle()
        #create new player and dealer hands (stored as global variables)
        global hand_dealer, hand_player
        hand_dealer = Hand()
        hand_player = Hand()
        hand_dealer.add_card(deck_inplay.deal_card())
        hand_player.add_card(deck_inplay.deal_card())
        hand_dealer.add_card(deck_inplay.deal_card())
        hand_player.add_card(deck_inplay.deal_card())


def hit():
    # replace with your code below
    global in_play, outcome, score, instruction
    
    # if the hand is in play, hit the player
    if (in_play == True) and ( hand_player.get_value() <= 21):
        hand_player.add_card(deck_inplay.deal_card())
        
        # if busted, assign a message to outcome, update in_play and score
        if hand_player.get_value() > 21:
            in_play = False
            outcome = "You went busted and lose"
            instruction = "New deal?"
            score -= 1


def stand():
    # replace with your code below
    global in_play, outcome, score, instruction
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        if hand_player.get_value() > 21:
            outcome ="You went busted and lose"
            instruction = "New deal?"
            in_play = False
        else:
            in_play = False
            while(hand_dealer.get_value() < 17):
                hand_dealer.add_card(deck_inplay.deal_card())
            
            
            if hand_dealer.get_value() > 21:
                outcome = " Dealer has busted and you win"
                instruction = "New deal?"
                score += 1
                in_play = False
            else:
                if (hand_dealer.get_value() >= hand_player.get_value()):
                    outcome = "You lose"
                    instruction = "New deal?"
                    score -= 1
                    in_play = False
                else:
                    outcome = "You win!"
                    instruction = "New deal?"
                    score += 1
                    in_play = False


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    hand_player.draw(canvas, [50, 400])
    hand_dealer.draw(canvas, [50, 200])
    
    #draw title blackjack
    canvas.draw_text('Black Jack', [100, 80], 40, 'White')
    canvas.draw_text('Score: ' + str(score), [450, 100],  25, 'Black')
    canvas.draw_text('Dealer', [50, 170], 30, 'Black')
    canvas.draw_text('Player', [50, 370], 30, 'Black')
    canvas.draw_text( outcome, [300, 170], 20, 'Black')
    canvas.draw_text( instruction, [300, 370], 20, 'Black')
    
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [(50 + CARD_BACK_CENTER[0]), (202 + CARD_BACK_CENTER[1])], CARD_BACK_SIZE)

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