import random
from collections import Counter
import turtle as trtl

from card_utils import Card, RANKS, standard_deck
from ui_common import setup_screen, register_common_shapes, make_button, make_text, write_text

HAND_SIZE = 7
DIFFICULTIES = ("easy", "medium", "hard")


def draw_card(hand: list[Card], deck: list[Card]) -> Card | None:
  if deck:
    card = deck.pop()
    hand.append(card)
    return card
  return None


def remove_books(hand: list[Card]) -> int:
  count = Counter(card.rank for card in hand)
  books = 0
  for rank, qty in list(count.items()):
    if qty == 4:
      hand[:] = [c for c in hand if c.rank != rank]
      books += 1
  return books


def transfer_cards(src: list[Card], dst: list[Card], rank: str) -> list[Card]:
  moving = [c for c in src if c.rank == rank]
  for c in moving:
    src.remove(c)
    dst.append(c)
  return moving


class GoFishAI:
  def __init__(self, difficulty: str):
    self.difficulty = difficulty
    self.memory: Counter[str] = Counter()

  def note_player_request(self, rank: str):
    self.memory[rank] += 1

  def remember_seen(self, cards: list[Card]):
    for c in cards:
      self.memory[c.rank] += 1

  def choose_rank(self, ai_hand: list[Card]) -> str:
    ranks_in_hand = Counter(card.rank for card in ai_hand)
    if self.difficulty == "easy":
      return random.choice(list(ranks_in_hand.keys()))
    if self.difficulty == "medium":
      strong = [r for r, qty in ranks_in_hand.items() if qty >= 2]
      return random.choice(strong) if strong else random.choice(list(ranks_in_hand.keys()))
    if self.memory:
      candidate = self.memory.most_common(1)[0][0]
      if candidate in ranks_in_hand:
        return candidate
    return max(ranks_in_hand.items(), key=lambda kv: kv[1])[0]


class GoFishUI:
  def __init__(self):
    self.wn = setup_screen("Go Fish")
    register_common_shapes()
    self.difficulty = "medium"
    self.deck: list[Card] = []
    self.player_hand: list[Card] = []
    self.ai_hand: list[Card] = []
    self.player_books = 0
    self.ai_books = 0
    self.ai_agent = GoFishAI(self.difficulty)
    self.player_turn = True
    self.game_over = False

    self.info = make_text((0, 320), size=18)
    self.status = make_text((0, 280), size=14)
    self.hand_text = make_text((-50, -260), size=12)
    self.deck_text = make_text((300, 320), size=12)
    self.books_text = make_text((-300, 320), size=12)
    self.next_btn = make_button("Next Turn", (0, -320), self.next_turn)
    self.diff_btn = make_button("Difficulty: medium", (0, -260), self.toggle_diff, width=3.2)

    self.reset_game()

  def toggle_diff(self, *_):
    idx = DIFFICULTIES.index(self.difficulty)
    self.difficulty = DIFFICULTIES[(idx + 1) % len(DIFFICULTIES)]
    self.ai_agent.difficulty = self.difficulty
    write_text(self.status, f"Difficulty set to {self.difficulty}")
    self.diff_btn.onclick(None)
    self.diff_btn = make_button(f"Difficulty: {self.difficulty}", (0, -260), self.toggle_diff, width=3.2)

  def reset_game(self):
    self.deck = standard_deck()
    self.player_hand = [self.deck.pop() for _ in range(HAND_SIZE)]
    self.ai_hand = [self.deck.pop() for _ in range(HAND_SIZE)]
    self.player_books = 0
    self.ai_books = 0
    self.ai_agent = GoFishAI(self.difficulty)
    self.player_turn = True
    self.game_over = False
    write_text(self.info, "Go Fish - your turn")
    self.update_ui()

  def update_ui(self, message: str = ""):
    write_text(self.hand_text, f"Your hand: {[c.rank for c in self.player_hand]}")
    write_text(self.deck_text, f"Deck: {len(self.deck)} left")
    write_text(self.books_text, f"Books - You: {self.player_books} | AI: {self.ai_books}")
    if message:
      write_text(self.status, message)

  def ask_player_rank(self) -> str | None:
    if not self.player_hand:
      return None
    ranks = sorted(set(c.rank for c in self.player_hand))
    prompt = f"Choose a rank to ask for {ranks}:"
    rank = self.wn.textinput("Your turn", prompt)
    if not rank:
      return None
    rank = rank.strip().lower()
    if rank not in ranks:
      write_text(self.status, "Pick a rank you hold.")
      return None
    return rank

  def player_turn_logic(self):
    rank = self.ask_player_rank()
    if not rank:
      return
    self.ai_agent.note_player_request(rank)
    taken = transfer_cards(self.ai_hand, self.player_hand, rank)
    books = remove_books(self.player_hand)
    self.player_books += books
    if taken:
      self.update_ui(f"You take {len(taken)} card(s) of {rank}. Go again.")
      return
    drawn = draw_card(self.player_hand, self.deck)
    if drawn:
      msg = f"Go fish... drew {drawn.label()}."
      if drawn.rank == rank:
        msg += " You drew your rank, go again."
        books += remove_books(self.player_hand)
        self.player_books += books
        self.update_ui(msg)
        return
    else:
      msg = "Deck empty."
    self.update_ui(msg)
    self.player_turn = False

  def ai_turn_logic(self):
    if not self.ai_hand and self.deck:
      draw_card(self.ai_hand, self.deck)
      return
    if not self.ai_hand:
      self.player_turn = True
      return
    rank = self.ai_agent.choose_rank(self.ai_hand)
    write_text(self.status, f"AI asks: any {rank}s?")
    given = transfer_cards(self.player_hand, self.ai_hand, rank)
    if given:
      self.ai_agent.remember_seen(given)
      books = remove_books(self.ai_hand)
      self.ai_books += books
      self.update_ui(f"AI took {len(given)} card(s) of {rank}. AI goes again.")
      return
    drawn = draw_card(self.ai_hand, self.deck)
    if drawn and drawn.rank == rank:
      books = remove_books(self.ai_hand)
      self.ai_books += books
      self.update_ui("AI drew their rank and goes again.")
      return
    self.player_turn = True
    self.update_ui("AI says go fish.")

  def check_end(self) -> bool:
    if not self.deck and not self.player_hand and not self.ai_hand:
      if self.player_books > self.ai_books:
        write_text(self.info, "You win Go Fish!")
      elif self.ai_books > self.player_books:
        write_text(self.info, "AI wins Go Fish.")
      else:
        write_text(self.info, "Go Fish tie.")
      write_text(self.status, "Click Next Turn to start a new game.")
      self.game_over = True
      return True
    return False

  def next_turn(self, *_):
    if self.game_over:
      self.reset_game()
      return
    if self.check_end():
      return
    if self.player_turn:
      self.player_turn_logic()
    else:
      self.ai_turn_logic()
    self.check_end()


def main():
  GoFishUI()
  trtl.done()


if __name__ == "__main__":
  main()
