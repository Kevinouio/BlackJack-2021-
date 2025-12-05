from pathlib import Path
import random as rand
import turtle as trtl

# Card order controls both the deck contents and the image lookup.
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

# Initializes the picture of the shapes that will be used in the project.
play_again_box = str(UI_DIR / 'play_again.gif')
rules_box = str(UI_DIR / 'rules.gif')
stand_box = str(UI_DIR / 'stand.gif')
hit_box = str(UI_DIR / 'hit.gif')

# Background from https://photostockeditor.com/image-rf/poker-table-felt-background-510657755
background = str(UI_DIR / 'Playing_card_Background.gif')

# Images of the card created by Bryon Knoll https://opengameart.org/content/playing-cards-vector-png
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
cards_images = [card_image_lookup[name] for name in card_names]

# creates the shapes of the cards that will be used along with the background.
wn.bgpic(background)
for shape in [play_again_box, rules_box, stand_box, hit_box, back_of_card] + cards_images:
  wn.addshape(shape)


# expands the list so that it can be the same amount as a normal deck of cards also shuffles the cards so it is a random card when you pull from it
def setup_deck(cards, re):
  cards_list = []
  # Creates a full deck of cards consisting of only spades
  while re < 4:
    cards_list += cards
    re += 1
  # Shuffles the hand
  rand.shuffle(cards_list)
  return cards_list

# The function sets up the board with the cards for both the dealer and the
def set_up_board():
  wn.tracer(False)
  player_turn = True
  repeats = 0
  x = -75
  y = -200
  # this loop passes the cards for the user(the player) for them to use for the game
  while repeats < 2:
    pass_cards('card' + str(repeats), x, y, player_turn)
    repeats += 1
    x = x * -1

  player_turn = False
  y = y * -1
  dealer_cards_setup(x, y, player_turn)
  create_stack()
  player_turn = True
  wn.tracer(True)

# this function calculates the amount of value you hand is
def insert_values(current_index, curr_turn):
  # If the cards is a jack, queen, or king, the value of 9 will be stored.
  if current_index > 9:
    current_index = 9
  # If the cards drawn is an ace, the index will be set to 11
  if current_index == 0:
    current_index = 10
  # adds the number to the user's hand value
  if curr_turn == True:
    player_card_values.append(current_index + 1)
  # Adds a value to the dealer's hand value
  else:
    dealer_card_values.append(current_index + 1)

# Creates an illusion of an stack of cards at the center of the board
def create_stack():
  deck = trtl.Turtle()
  deck.penup()
  deck.goto(0, 0)
  deck.shape(back_of_card)

# This sets up the boards with all the cards for the dealer and the user
def dealer_cards_setup(x, y, curr_turn):
  card = trtl.Turtle()
  card.penup()
  card_img = cards_list.pop(0)
  index = card_names.index(card_img)
  card.shape(back_of_card)
  insert_values(index, curr_turn)
  card.goto(x, y)
  dealer_cards.append(card)
  x = x * -1
  pass_cards(card, x, y, curr_turn)
  print(dealer_card_values)

# Passes the cards to the player or the dealer.
def pass_cards(card, x, y, curr_player):
  card = trtl.Turtle()
  card.penup()
  card_img = cards_list.pop(0)
  index = card_names.index(card_img)
  shape = cards_images.pop(index)
  card.shape(shape)
  cards_images.insert(index, shape)
  card.goto(x, y)
  insert_values(index, curr_player)
  # If it is passing to the user, add the card to the list of cards for the user
  if curr_player == True:
    player_cards.append(card)
  # If it is passing to the dealer, add the card to the list of cards for the dealer
  else:
    dealer_cards.append(card)
  return index

# Draws the card for either the user or the dealer.
def draw_card(card_set, curr_turn):
  x = -200
  card = trtl.Turtle()
  card.penup()
  card_img = cards_list.pop(0)
  index = card_names.index(card_img)
  shape = cards_images.pop(index)
  card.shape(shape)
  cards_images.insert(index, shape)
  insert_values(index, curr_turn)
  card_set.append(card)
  # if it is the player's turn, put the cards in line with the user, else if it is the dealer's turn,
  # pass the cards in line with the dealer
  if curr_turn == True:
    y = -200
  else:
    y = 200
  # Fans out the cards to be visually appealing.
  for cards in card_set:
    x_spaced = 300 / len(card_set)
    x = x + x_spaced
    cards.goto(x, y)

# This will determine who will draw the cards when the user clicks hit or stand
def determine_draw(x, y):
  global player_turn
  player_sum = check_player(player_card_values, player_turn, 0)
  # If the user had clicked the hit button, the player will draw the card
  if x < 0:
    draw_card(player_cards, player_turn)
    check_player(player_card_values, player_turn, 0)
  # If the user had clicked the stand buttong, the player will stop drawing cards and the dealer will draw cards.
  elif x > 0:
    dealer_draw(player_sum)


# runs a function to run until the dealer has a higher value than the player or has a hand value over 21
def dealer_draw(sum_values):
  player_turn = False
  sum_dealer = 0
  flip_dealer_card()
  # Gets the current value of the dealer's hand with only two cards.
  for values in dealer_card_values:
    sum_dealer += values
  finish_drawing()
  text.write('Dealers Turn', align='center', font=('Verdana', 20, 'bold'))
  check_player(dealer_card_values, player_turn, sum_values)
  # The dealer will keep drawing cards until the value gets above the user's hand value.
  while sum_dealer < sum_values:
    draw_card(dealer_cards, player_turn)
    sum_dealer = check_player(dealer_card_values, player_turn, sum_values)
  check_player(dealer_card_values, player_turn, sum_values)

# flips over the card that the dealer has flipped over
def flip_dealer_card():
  index = dealer_card_values[0] - 1
  dealer_cards[0].shape(cards_images[index])


# this function would determine the
def check_player(list_values, player_turn, player_sum):
  # calculates for the sum of the hand that it is asked for
  sum_values = 0
  for values in list_values:
    sum_values = values + sum_values

  # recalculates the value of the hand if there is an ace in the hand to an 11 to a 1
  if sum_values > 21:
    for values in range(len(list_values)):
      if list_values[values] == 11:
        list_values[values] = 1
        sum_values = 0
        for values in list_values:
          sum_values = values + sum_values
  # Determines if the player had went over 21 in hand value
  if player_turn == True:
    player_total = sum_values
    player_hand_value.clear()
    player_hand_value.write('Player Hand  \n Value: ' + str(sum_values), align='center', font=('Verdana', 20, 'bold'))
    if sum_values > 21:
      finish_drawing()
      text.write('You went over 21 \n You Lost', align='center', font=('Verdana', 20, 'bold'))
      flip_dealer_card()
      play_again.showturtle()
    return player_total
  # Determines the winner of the round
  elif player_turn == False:
    dealer_hand_value.clear()
    dealer_hand_value.write('Dealer Hand  \n Value: ' + str(sum_values), align='center', font=('Verdana', 20, 'bold'))
    # The User had won the game with a closer value to 21
    if sum_values > 21:
      text.clear()
      text.write('You won \n You were closer to 21 than the dealer', align='center', font=('Verdana', 20, 'bold'))
      play_again.showturtle()
    # The user and the dealer had gotten to a value exactaly as the same as the dealer.
    elif player_sum == sum_values:
      text.clear()
      text.write('You tied \n The dealer has the same value of cards as you', align='center', font=('Verdana', 20, 'bold'))
      play_again.showturtle()
    # The dealer won with a value closer to 21
    elif player_sum < sum_values:
      text.clear()
      text.write('You lost \n The Dealer got closer to 21', align='center', font=('Verdana', 20, 'bold'))
      play_again.showturtle()
    return sum_values

# the buttons and the text telling the player turn dissapears to show no moves for you to do.
def finish_drawing():
  hit.hideturtle()
  stand.hideturtle()
  text.clear()

# this would reset the whole game in order to play another round of blackjack
def restart_game(x, y):
  wn.tracer(False)
  global player_cards, dealer_cards, player_card_values, dealer_card_values, cards_list

  # these loops would remove and hide the cards that were on the screen in the previous game
  for cards in player_cards:
    cards.hideturtle()
  for cards in dealer_cards:
    cards.hideturtle()

  # resets all the value to the original value to be able to restart the game.
  player_cards = []
  dealer_cards = []
  player_card_values = []
  dealer_card_values = []
  cards_list = setup_deck(card_names, repeats)
  set_up_board()
  stand.showturtle()
  hit.showturtle()
  text.clear()
  player_hand_value.clear()
  dealer_hand_value.clear()
  player_hand_value.write('Player Hand  \n Value: ', align='center', font=('Verdana', 20, 'bold'))
  text.write('Would you like to hit or stand', align='center', font=('Verdana', 20, 'bold'))
  play_again.hideturtle()
  check_player(player_card_values, player_turn, sum_values)
  wn.tracer(True)


wn.tracer(False)
cards_list = setup_deck(card_names, repeats)

# Creates a text area for which the game is going to indicate to the user of what the user can do at the moment
text = trtl.Turtle()
text.hideturtle()
text.color('white')
text.penup()
text.goto(0, 300)
text.write('Would you like to hit or stand', align='center', font=('Verdana', 20, 'bold'))

# Creates a button for the player to draw a card
hit = trtl.Turtle()
hit.penup()
hit.goto(-75, -350)
hit.shape(hit_box)

# Creates a button for the user to click on for it to switch to the dealer's turn
stand = trtl.Turtle()
stand.penup()
stand.goto(75, -350)
stand.shape(stand_box)

# Creates a box that shows the rules of the game
rules = trtl.Turtle()
rules.penup()
rules.shape(rules_box)
rules.goto(350, 0)

# Gives the user a way to know their value of their hand without having to do their own math.
player_hand_value = trtl.Turtle()
player_hand_value.hideturtle()
player_hand_value.penup()
player_hand_value.goto(-300, -200)
player_hand_value.color('white')
player_hand_value.write('Player Hand  \n Value: ', align='center', font=('Verdana', 20, 'bold'))

# Shows the dealer's hand value for you to also make sure that either you lost or won the round
dealer_hand_value = trtl.Turtle()
dealer_hand_value.hideturtle()
dealer_hand_value.penup()
dealer_hand_value.goto(-300, 200)
dealer_hand_value.color('white')

# Creates a button for the user to click if you/the user would like to play another round
play_again = trtl.Turtle()
play_again.penup()
play_again.hideturtle()
play_again.penup()
play_again.shape(play_again_box)
play_again.goto(-150, 0)

# start to setup the board for the game to happen
set_up_board()

# allows for the clicks to happen in the interface on the button.
hit.onclick(determine_draw)
stand.onclick(determine_draw)
play_again.onclick(restart_game)

wn.mainloop()
