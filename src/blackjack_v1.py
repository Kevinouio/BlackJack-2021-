from pathlib import Path
import turtle as trtl
import random as rand

card_names = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.parent / 'assets'
CARDS_DIR = ASSETS_DIR / 'cards'

wn = trtl.Screen()
repeats = 0

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

for shape in card_image_lookup.values():
  wn.addshape(shape)
cards_images = [card_image_lookup[name] for name in card_names]


#expands the list so that it can be the same amount as a normal deck of cards
def setup_deck(cards, re):
  cards_list = []
  while re < 2:
    cards_list += cards
    re += 1
  rand.shuffle(cards_list)
  return cards_list
cards_list = setup_deck(card_names, repeats)

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
  index = card_names.index(card_img)
  shape =  cards_images.pop(index)
  card.shape(shape)
  cards_images.insert(index, shape)
  card.goto(x,y)
  print(cards_images)
set_up_board()

wn.mainloop()
