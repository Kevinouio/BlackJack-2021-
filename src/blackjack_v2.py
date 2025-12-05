from pathlib import Path
import turtle as trtl
import random as rand

card_names = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.parent / 'assets'
CARDS_DIR = ASSETS_DIR / 'cards'
UI_DIR = ASSETS_DIR / 'ui'

player_cards = []
dealer_cards = []
player_card_values = []
dealer_card_values = []
player_turn = True
wn = trtl.Screen()
wn.setup(width=1000, height=800)
repeats = 0
sum_values = 0
rules_box = str(UI_DIR / 'rules.gif')
stand_box = str(UI_DIR / 'stand.gif')
background = str(UI_DIR / 'Playing_card_Background.gif')
back_of_card = str(CARDS_DIR / 'Back_of_playing_card.gif')
card_image_lookup = {
  'ace': str(CARDS_DIR / 'ace_of_clubs.gif'),
  '2': str(CARDS_DIR / '2_of_clubs.gif'),
  '3': str(CARDS_DIR / '3_of_clubs.gif'),
  '4': str(CARDS_DIR / '4_of_clubs.gif'),
  '5': str(CARDS_DIR / '5_of_clubs.gif'),
  '6': str(CARDS_DIR / '6_of_clubs.gif'),
  '7': str(CARDS_DIR / '7_of_clubs.gif'),
  '8': str(CARDS_DIR / '8_of_clubs.gif'),
  '9': str(CARDS_DIR / '9_of_clubs.gif'),
  '10': str(CARDS_DIR / '10_of_clubs.gif'),
  'jack': str(CARDS_DIR / 'jack_of_clubs2.gif'),
  'queen': str(CARDS_DIR / 'queen_of_clubs2.gif'),
  'king': str(CARDS_DIR / 'king_of_clubs2.gif'),
}
hit_box = str(UI_DIR / 'hit.gif')

wn.bgpic(background)
for shape in [rules_box, stand_box, hit_box, back_of_card] + [card_image_lookup[name] for name in card_names]:
  wn.addshape(shape)
cards_images = [card_image_lookup[name] for name in card_names]


#expands the list so that it can be the same amount as a normal deck of cards
def setup_deck(cards, re):
  cards_list = []
  while re < 4:
    cards_list += cards
    re += 1
  rand.shuffle(cards_list)
  return cards_list

def set_up_board():
  wn.tracer(False)
  player_turn = True
  repeats = 0
  x = -75
  y = -200
  while repeats < 2:
    pass_cards('card' + str(repeats),x,y,player_turn)
    repeats += 1
    x = x * -1
  player_turn = False
  y = y * -1
  dealer_cards_setup(x,y,player_turn)
  create_stack()
  player_turn = True
  wn.tracer(True)

def insert_values(current_index, curr_turn):
  if current_index > 9:
    current_index = 9
  if current_index == 0:
    current_index = 10
  if curr_turn == True:
    player_card_values.append(current_index + 1)
  else:
    dealer_card_values.append(current_index + 1)

def create_stack():
  deck = trtl.Turtle()
  deck.penup()
  deck.goto(0,0)
  deck.shape(back_of_card)

def dealer_cards_setup(x,y,curr_turn):
  card = trtl.Turtle()
  card.penup()
  card_img = cards_list.pop(0)
  index = card_names.index(card_img)
  card.shape(back_of_card)
  insert_values(index,curr_turn)
  card.goto(x,y)
  dealer_cards.append(card)
  x = x * -1
  pass_cards(card,x,y,curr_turn)

def pass_cards(card, x, y,curr_player):
  try:
    card = trtl.Turtle()
    card.penup()
    card_img = cards_list.pop(0)
    index = card_names.index(card_img)
    shape =  cards_images.pop(index)
    card.shape(shape)
    cards_images.insert(index, shape)
    card.goto(x,y)
    insert_values(index,curr_player)
    if curr_player ==True:
      player_cards.append(card)
    else:
      dealer_cards.append(card)
    return index
  except:
    print(card_img)
    print(index)
    print(cards_list)

def draw_card(card_set,curr_turn):
  x = -200
  card = trtl.Turtle()
  card.penup()
  card_img = cards_list.pop(0)
  index = card_names.index(card_img)
  shape = cards_images.pop(index)
  card.shape(shape)
  cards_images.insert(index, shape)
  insert_values(index,curr_turn)
  card_set.append(card)  
  if curr_turn == True:
    y= -200
  else:
    y= 200
  for cards in card_set:
    x_spaced = 300/len(card_set)
    x = x + x_spaced
    cards.goto(x,y)
  

def determine_draw(x,y):
  global player_turn
  player_sum = check_player(player_card_values, player_turn, 0)
  if x < 0:
    draw_card(player_cards, player_turn)
    check_player(player_card_values, player_turn, 0)    
  elif x > 0:
    dealer_draw(player_sum)
  
  print(player_card_values)
  print(dealer_card_values)

#runs a function to run until the dealer has a higher value cards than the dealer.
def dealer_draw(sum_values):
  player_turn = False
  sum_dealer = 0
  flip_dealer_card()
  for values in dealer_card_values:
    sum_dealer += values 
  finish_drawing()
  text.write('Dealers Turn', align='center', font=('Verdana',20,'bold'))
  while sum_dealer < sum_values: #sum of values is currently undefined fix this next time
    draw_card(dealer_cards,player_turn)
    sum_dealer = check_player(dealer_card_values, player_turn, sum_values)
  check_player(dealer_card_values, player_turn, sum_values)
  
def flip_dealer_card():
  index = dealer_card_values[0] - 1
  dealer_cards[0].shape(cards_images[index])


def check_player(list_values, player_turn, player_sum):
  sum_values = 0
  for values in list_values:
    sum_values = values + sum_values
  if sum_values > 21:
    for values in range(len(list_values)):
      if list_values[values] == 11:
        list_values[values] = 1
        for values in list_values:
          sum_values = 0
          sum_values = values + sum_values
  if player_turn == True:
    player_total = sum_values
    if sum_values > 21:
      finish_drawing()
      text.write('You went over 21 \n You Lost', align='center', font=('Verdana',20,'bold'))
      flip_dealer_card()
    elif sum_values == 21:
      finish_drawing()
      text.write('Blackjack you hit 21 \n You Won', align='center', font=('Verdana',20,'bold'))
      flip_dealer_card()
    return player_total
  elif player_turn == False:
    if sum_values > 21:
      text.clear()
      text.write('You won \n You were closer to 21 than the dealer', align='center', font=('Verdana',20, 'bold'))
    elif player_sum == sum_values:
      text.clear()
      text.write('You tied \n The dealer has the same value of cards as you', align='center', font=('Verdana',20,'bold'))
    elif player_sum < sum_values:
      text.clear()
      text.write('You lost \n The Dealer got closer to 21', align='center', font=('Verdana',20,'bold'))
    return sum_values



def finish_drawing():
  hit.hideturtle()
  stand.hideturtle()
  text.clear()
cards_list = setup_deck(card_names, repeats) 
set_up_board()

wn.tracer(False)
text = trtl.Turtle()
text.hideturtle()
text.penup()
text.goto(0,300)
text.write('Would you like to hit or stand', align='center', font=('Verdana',20,'bold'))

hit = trtl.Turtle()
hit.penup()
hit.goto(-75,-350)
hit.shape(hit_box)

stand = trtl.Turtle()
stand.penup()
stand.goto(75,-350)
stand.shape(stand_box)

rules = trtl.Turtle()
rules.penup()
rules.shape(rules_box)
rules.goto(350,0)

player_hand_value = trtl.Turtle()
player_hand_value.hideturtle()
player_hand_value.penup()
player_hand_value.goto(-200,-200)
player_hand_value.color('white')


wn.tracer(True)


hit.onclick(determine_draw)
stand.onclick(determine_draw)
wn.mainloop()
