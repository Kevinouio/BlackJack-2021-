import turtle as trtl
import random as rand

spades_list = ['ace_of_spades', '2_of_spades', '3_of_spades', '4_of_spades', '5_of_spades', '6_of_spades', '7_of_spades', '8_of_spades', 
'9_of_spades', '10_of_spades', 'jack_of_spades', 'queen_of_spades', 'king_of_spades']
wn = trtl.Screen()
repeats = 0

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
cards_images = [ace_spades, two_spades, three_spades, four_spades, five_spades, six_spades, seven_spades, eight_spades, nine_spades, ten_spades, jack_spades, queen_spades, king_spades]


#expands the list so that it can be the same amount as a normal deck of cards
def setup_deck(cards, re):
  cards_list = []
  while re < 2:
    cards_list += cards
    re += 1
  rand.shuffle(cards_list)
  return cards_list
cards_list = setup_deck(spades_list, repeats)

def set_up_board():
  wn.tracer(False)
  repeats = 0
  x = -75
  y = -200
  while repeats < 4:
    pass_cards('card' + str(repeats),x,y)
    repeats += 1
    x = x * -1
    if repeats == 2:
      y = y * -1
  wn.tracer(True)

def pass_cards(card, x, y):
  card = trtl.Turtle()
  card.penup()
  card_img = cards_list.pop(0)
  index = spades_list.index(card_img)
  shape =  cards_images.pop(index)
  card.shape(shape)
  cards_images.insert(index, shape)
  card.goto(x,y)
  print(cards_images)
set_up_board()

wn.mainloop()