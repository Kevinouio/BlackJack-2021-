import random
from collections import Counter
import turtle as trtl

from card_utils import Card, SUITS, standard_deck
from ui_common import setup_screen, register_common_shapes, make_button, make_text, write_text

HAND_SIZE = 5
DIFFICULTIES = ("easy", "medium", "hard")


def playable_cards(hand: list[Card], current_suit: str, current_rank: str) -> list[Card]:
  return [c for c in hand if c.rank == "8" or c.rank == current_rank or c.suit == current_suit]


def choose_ai_card(hand: list[Card], current_suit: str, current_rank: str, difficulty: str) -> tuple[Card | None, str | None]:
  options = playable_cards(hand, current_suit, current_rank)
  if not options:
    return None, None
  if difficulty == "easy":
    return random.choice(options), None

  if difficulty == "medium":
    non_wild = [c for c in options if c.rank != "8"]
    pick = random.choice(non_wild) if non_wild else random.choice(options)
    new_suit = None
    if pick.rank == "8":
      counts = Counter(c.suit for c in hand if c.rank != "8")
      new_suit = counts.most_common(1)[0][0] if counts else random.choice(SUITS)
    return pick, new_suit

  non_wild = [c for c in options if c.rank != "8"]
  if non_wild:
    suit_counts = Counter(c.suit for c in hand if c.rank != "8")
    best_suit = suit_counts.most_common(1)[0][0]
    prioritized = [c for c in non_wild if c.suit == best_suit] or non_wild
    pick = max(prioritized, key=lambda c: c.value)
    return pick, None
  suit_counts = Counter(c.suit for c in hand if c.rank != "8")
  new_suit = suit_counts.most_common(1)[0][0] if suit_counts else random.choice(SUITS)
  return options[0], new_suit


class CrazyEightsUI:
  def __init__(self):
    self.wn = setup_screen("Crazy Eights")
    register_common_shapes()
    self.difficulty = "medium"
    self.deck: list[Card] = []
    self.player: list[Card] = []
    self.ai: list[Card] = []
    self.top: Card | None = None
    self.current_suit: str = ""
    self.current_rank: str = ""
    self.player_turn = True
    self.game_over = False

    self.info = make_text((0, 320), size=18)
    self.status = make_text((0, 280), size=14)
    self.hand_text = make_text((-50, -260), size=12)
    self.top_text = make_text((0, 200), size=14)
    self.next_btn = make_button("Play Turn", (0, -320), self.play_turn)
    self.diff_btn = make_button("Difficulty: medium", (0, -260), self.toggle_diff, width=3.2)

    self.reset_game()

  def toggle_diff(self, *_):
    idx = DIFFICULTIES.index(self.difficulty)
    self.difficulty = DIFFICULTIES[(idx + 1) % len(DIFFICULTIES)]
    write_text(self.status, f"Difficulty set to {self.difficulty}")
    self.diff_btn.onclick(None)
    self.diff_btn = make_button(f"Difficulty: {self.difficulty}", (0, -260), self.toggle_diff, width=3.2)

  def reset_game(self):
    deck = standard_deck()
    self.deck = deck
    self.player = [self.deck.pop() for _ in range(HAND_SIZE)]
    self.ai = [self.deck.pop() for _ in range(HAND_SIZE)]
    self.top = self.deck.pop()
    while self.top.rank == "8":
      random.shuffle(self.deck)
      self.top = self.deck.pop()
    self.current_rank = self.top.rank
    self.current_suit = self.top.suit
    self.player_turn = True
    self.game_over = False
    write_text(self.info, "Crazy Eights - your turn")
    self.update_ui("Starting card placed.")

  def update_ui(self, message: str = ""):
    write_text(self.hand_text, f"Your hand: {[f'{i}:{c.rank[0]}{c.suit[0]}' for i,c in enumerate(self.player)]}")
    write_text(self.top_text, f"Top card: {self.current_rank} of {self.current_suit} | Deck {len(self.deck)}")
    if message:
      write_text(self.status, message)

  def player_action(self):
    options = playable_cards(self.player, self.current_suit, self.current_rank)
    if not options:
      if self.deck:
        drawn = self.deck.pop()
        self.player.append(drawn)
        self.update_ui(f"No play. Drew {drawn.label()}.")
      else:
        self.update_ui("No play and deck empty.")
      self.player_turn = False
      return
    choice = self.wn.textinput("Your move", "Enter card index to play or 'd' to draw:")
    if choice is None:
      return
    choice = choice.strip().lower()
    if choice == "d":
      if self.deck:
        drawn = self.deck.pop()
        self.player.append(drawn)
        self.update_ui(f"Drew {drawn.label()}.")
      else:
        self.update_ui("Deck empty; cannot draw.")
      self.player_turn = False
      return
    try:
      idx = int(choice)
      card = self.player[idx]
    except (ValueError, IndexError):
      self.update_ui("Invalid choice.")
      return
    if card not in options:
      self.update_ui("That card can't be played now.")
      return
    self.player.remove(card)
    self.top = card
    self.current_rank = card.rank
    self.current_suit = card.suit
    if card.rank == "8":
      suit_choice = self.wn.textinput("Wild 8", f"Choose suit {SUITS}:")
      if suit_choice not in SUITS:
        suit_choice = random.choice(SUITS)
      self.current_suit = suit_choice
      self.current_rank = "8"
    self.update_ui(f"You played {card.label()}.")
    self.player_turn = False

  def ai_action(self):
    options = playable_cards(self.ai, self.current_suit, self.current_rank)
    if not options:
      if self.deck:
        self.ai.append(self.deck.pop())
      self.player_turn = True
      self.update_ui("AI draws.")
      return
    card, new_suit = choose_ai_card(self.ai, self.current_suit, self.current_rank, self.difficulty)
    if not card:
      self.player_turn = True
      return
    self.ai.remove(card)
    self.top = card
    self.current_rank = card.rank
    self.current_suit = card.suit
    if card.rank == "8":
      self.current_suit = new_suit or random.choice(SUITS)
      self.current_rank = "8"
    self.player_turn = True
    self.update_ui(f"AI plays {card.label()} (suit now {self.current_suit}).")

  def check_end(self) -> bool:
    if not self.player:
      write_text(self.info, "You win!")
      self.game_over = True
      return True
    if not self.ai:
      write_text(self.info, "AI wins.")
      self.game_over = True
      return True
    if not self.deck and not playable_cards(self.player, self.current_suit, self.current_rank) and not playable_cards(self.ai, self.current_suit, self.current_rank):
      write_text(self.info, "Stalemate.")
      self.game_over = True
      return True
    return False

  def play_turn(self, *_):
    if self.game_over:
      self.reset_game()
      return
    if self.check_end():
      write_text(self.status, "Click Play Turn to start over.")
      return
    if self.player_turn:
      self.player_action()
    else:
      self.ai_action()
    self.check_end()


def main():
  CrazyEightsUI()
  trtl.done()


if __name__ == "__main__":
  main()
