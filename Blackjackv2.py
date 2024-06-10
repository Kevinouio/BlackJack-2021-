import turtle as trtl
import random as rand
import time

spades_list = ['ace_of_spades', '2_of_spades', '3_of_spades', '4_of_spades', '5_of_spades', '6_of_spades', '7_of_spades', '8_of_spades', 
'9_of_spades', '10_of_spades', 'jack_of_spades', 'queen_of_spades', 'king_of_spades']
player_cards = []
dealer_cards = []
player_card_values = []
dealer_card_values = []
player_turn = True
wn = trtl.Screen()
wn.setup(width=1000, height=800)
repeats = 0
sum_values = 0
rules_box = 'Personal Projects/Card Games/rules.gif'
stand_box = 'Personal Projects/Card Games/stand.gif'
background = 'Personal Projects/Card Games/Playing_card_Background.gif'
back_of_card = 'Personal Projects/Card Games/Back_of_playing_card.gif'
ace_spades = 'Personal Projects/Card Games/ace_of_clubs.gif'
two_spades = 'Personal Projects/Card Games/2_of_clubs.gif'
three_spades = 'Personal Projects/Card Games/3_of_clubs.gif'
four_spades = 'Personal Projects/Card Games/4_of_clubs.gif'
five_spades = 'Personal Projects/Card Games/5_of_clubs.gif'
six_spades = 'Personal Projects/Card Games/6_of_clubs.gif'
seven_spades = 'Personal Projects/Card Games/7_of_clubs.gif'
eight_spades = 'Personal Projects/Card Games/8_of_clubs.gif'
nine_spades = 'Personal Projects/Card Games/9_of_clubs.gif'
ten_spades = 'Personal Projects/Card Games/10_of_clubs.gif'
jack_spades = 'Personal Projects/Card Games/jack_of_clubs2.gif'
queen_spades = 'Personal Projects/Card Games/queen_of_clubs2.gif'
king_spades = 'Personal Projects/Card Games/king_of_clubs2.gif'
hit_box = 'Personal Projects/Card Games/hit.gif'

wn.bgpic(background)
wn.addshape(rules_box)
wn.addshape(stand_box)
wn.addshape(hit_box)
wn.addshape(back_of_card)
wn.addshape(ace_spades)
wn.addshape(two_spades)
wn.addshape(three_spades)
wn.addshape(four_spades)
wn.addshape(five_spades)
wn.addshape(six_spades)
wn.addshape(seven_spades)
wn.addshape(eight_spades)
wn.addshape(nine_spades)
wn.addshape(ten_spades)
wn.addshape(jack_spades)
wn.addshape(queen_spades)
wn.addshape(king_spades)
cards_images = [ace_spades, two_spades, three_spades, four_spades, five_spades, six_spades, seven_spades, eight_spades, nine_spades, jack_spades, queen_spades, king_spades]


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
  index = spades_list.index(card_img)
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
    index = spades_list.index(card_img)
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
  index = spades_list.index(card_img)
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









cards_list = setup_deck(spades_list, repeats) 
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