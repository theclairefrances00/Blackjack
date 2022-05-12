from PIL import Image, ImageTk
import random
from random import shuffle

suits = ["spades",
         "hearts",
         "diamonds",
         "clubs"]

values = [None, None, '2','3','4','5',
          '6','7','8','9',
          '10','jack','queen',
          'king','ace']

deck = []

player_labels = []
dealer_labels = []

player_cards = []
dealer_cards = []

round_done = False

num_wins = 0
num_losses = 0

def resize_card(card):
    card_img = Image.open(card)
    card_img = card_img.resize((150//2,218//2))
    return ImageTk.PhotoImage(card_img)

def back_of_cards():
    return resize_card(f'cards/card_back.png')

def create_deck():
    for i in range(len(suits)):
        for j in range(2, len(values)):
            deck.append(f'{values[j]}_of_{suits[i]}')

def deal_cards():
    random.shuffle(deck)
    player_cards = []
    dealer_cards = []
    for i in range(2):
        cards = [deck.pop(),deck.pop()]
        player_cards.append([cards[0],resize_card(f'cards/{cards[0]}.png')])
        dealer_cards.append([cards[1],resize_card(f'cards/{cards[1]}.png')])
    return player_cards, dealer_cards

def clear_frame(window_frame): # destroy all widgets from frame
    for widget in window_frame.winfo_children():
       widget.destroy()

def get_score(cards):
    total_val = 0
    aces = 0
    for card in cards:
        val = card[0].split("_")[0]
        if val != 'ace':
            try:
                val = int(val)
            except ValueError: # Handle face cards
                val = 10
            total_val+=val
        else:
            aces+=1
    if total_val <= 10 and aces >0: # Handle ace as 11 or 1
        aces-=1
        total_val +=11
    if aces > 0:
        total_val+=aces
    return(total_val)

def show_dealer_cards():
    for i in range(len(dealer_cards)):
        dealer_labels[i].config(image = dealer_cards[i][1])
        
def check_winner(wins, losses, outcome):
    global num_wins, num_losses
    player_score = get_score(player_cards)
    dealer_score = get_score(dealer_cards)

    if dealer_score == 21 or (dealer_score >= player_score and dealer_score <= 21) or player_score > 21:
        outcome.config(text= "Dealer Wins", bg= "white")
        num_losses=num_losses+1
        losses.config(text="Losses: " + str(num_losses))
    else:
        #print("Player win")
        outcome.config(text= "You Win!", bg= "white")
        num_wins=num_wins+1
        wins.config(text="Wins: " + str(num_wins))
    show_dealer_cards()
    return num_wins, num_losses
      
def hit(wins, losses, player_points, dealer_points, outcome, player_cards):
    global round_done
    if round_done:
        pass
    else:
        card = deck.pop()
        player_cards.append([card,resize_card(f'cards/{card}.png')])
        
        if get_score(player_cards)>21:
            round_done = True
            check_winner(wins, losses, outcome)
            dealer_points.config(text= 'Dealer Points: '+ str(get_score(dealer_cards)))

    player_points.config(text= 'Your Points: '+ str(get_score(player_cards)))
    return player_cards, round_done

def stand(wins, losses, player_points, dealer_points, outcome):
    global round_done
    if round_done:
        pass
    else:
        round_done = True
        check_winner(wins, losses, outcome)
    player_points.config(text= 'Your Points: '+ str(get_score(player_cards)))
    dealer_points.config(text= 'Dealer Points: '+ str(get_score(dealer_cards)))
