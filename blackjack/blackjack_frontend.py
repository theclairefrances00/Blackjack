import blackjack_backend as bj
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.title("Blackjack")
window.configure(background="green")
window.geometry("900x450")

window_frame = Frame(window, bg="green")
window_frame.pack(pady=20)

back_of_cards = bj.back_of_cards()

def add_card_label(labels, frame, img, hide_cards):
    labels.append(Label(frame, text=''))
    num_labels = len(labels)-1
    if hide_cards:
        labels[num_labels].config(image=back_of_cards)
    else:
        labels[num_labels].config(image=img)
    labels[num_labels].grid(row=0, column=num_labels, pady=20,padx=20)
    return labels

def create_frames():
    player_frame = LabelFrame(window_frame, text="Player", bd=0)
    player_frame.grid(row=0, column=0, padx=20,ipadx=20)
    
    dealer_frame = LabelFrame(window_frame, text="Dealer", bd=0)
    dealer_frame.grid(row=0, column=1, padx=20,ipadx=20)

    button_frame = LabelFrame(window_frame, text="", bg="green")
    button_frame.grid(row=1, column=0, padx=20,pady=20)

    wins_frame = LabelFrame(window_frame, text="", bd=0)
    wins_frame.grid(row=2, column=1, padx=20,ipadx=20)

    points_frame = LabelFrame(window_frame, text="", bd=0)
    points_frame.grid(row=1, column=1, padx=20,ipadx=20)

    end_round_frame = LabelFrame(window_frame, text="", bg="green")
    end_round_frame.grid(row=2, column=0, padx=20,ipadx=20)

    return player_frame, dealer_frame, button_frame, wins_frame, points_frame, end_round_frame

def create_labels(wins_frame, points_frame, end_round_frame):
    wins = Label(wins_frame, text='Wins: ' + str(bj.num_wins), font=("Helvetica", 10))
    wins.grid(row=0, column=0)

    losses = Label(wins_frame, text='Losses: ' + str(bj.num_losses), font=("Helvetica", 10))
    losses.grid(row=1, column=0)

    player_points = Label(points_frame, text='Your Points: '+ str(bj.get_score(bj.player_cards)), font=("Helvetica", 12))
    player_points.grid(row=0, column=0)

    dealer_points = Label(points_frame, text='Dealer Points: ', font=("Helvetica", 12))
    dealer_points.grid(row=1, column=0)
    
    outcome = Label(end_round_frame, text="", font=("Helvetica", 12),bg="green")
    outcome.grid(row=0, column=1, padx=20,pady=20)

    return wins, losses,  player_points, dealer_points, outcome

def create_buttons(button_frame, player_frame, dealer_frame, end_round_frame, wins, losses, player_points, dealer_points, outcome):
    stand_button = Button(button_frame, text="Stand", font=("Helvetica", 14), command=lambda :bj.stand(wins, losses, player_points, dealer_points,outcome))
    stand_button.grid(row=0,column=0, padx=20,pady=20)

    hit_button = Button(button_frame, text="Hit", font=("Helvetica", 14), command=lambda :hit(wins, losses,player_points, dealer_points,outcome, bj.player_cards, player_frame))
    hit_button.grid(row=0,column=1, padx=20,pady=20)

    play_again_button = Button(end_round_frame, text="Play again", font=("Helvetica", 12), command=lambda :start_game(window_frame, False))
    play_again_button.grid(row=0,column=0, padx=20,pady=20)
    
def start_game(window_frame, first_round):
    bj.clear_frame(window_frame)
    bj.round_done = False
    
    if first_round or len(bj.deck)<=8:
        bj.create_deck()

    bj.player_cards, bj.dealer_cards = bj.deal_cards()
    bj.player_labels = []
    bj.dealer_labels = []
    player_frame, dealer_frame, button_frame, wins_frame, points_frame, end_round_frame = create_frames()

    for i in range(2):
        add_card_label(bj.player_labels, player_frame, bj.player_cards[i][1], False)
        add_card_label(bj.dealer_labels, dealer_frame, bj.dealer_cards[i][1], True)
    
    wins, losses,  player_points, dealer_points, outcome = create_labels(wins_frame, points_frame, end_round_frame)
    create_buttons(button_frame, player_frame, dealer_frame, end_round_frame, wins, losses, player_points, dealer_points, outcome)

def hit(wins, losses,player_points, dealer_points,outcome, player_cards, player_frame): 
    player_cards, round_done = bj.hit(wins, losses,player_points, dealer_points,outcome, bj.player_cards)
    
    if len(bj.player_labels) < len(player_cards):
        add_card_label(bj.player_labels, player_frame, bj.player_cards[len(player_cards)-1][1], False)

# Initial frame
Label(window_frame, text='Welcome to Blackjack', font=("Helvetica", 16)).grid(row=0, column=0, pady=20)
play_button = Button(window_frame, text="Play", font=("Helvetica", 14), command=lambda :start_game(window_frame, True))
play_button.grid(row=1, column=0)
  
window.mainloop()
