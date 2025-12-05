from collections import deque
import random
import turtle as trtl

from card_utils import Card, standard_deck
from ui_common import setup_screen, register_common_shapes, make_button, make_text, write_text

DIFFICULTIES = ("easy", "medium", "hard")


class WarUI:
  def __init__(self):
    self.wn = setup_screen("War")
    register_common_shapes()
    self.difficulty = "medium"
    self.deck = deque(standard_deck())
    self.player_pile = deque()
    self.ai_pile = deque()
    self.deal()
    self.round_no = 0
    self.game_over = False

    self.info = make_text((0, 320), size=18)
    self.status = make_text((0, 260), size=14)
    self.player_count = make_text((-300, -250), size=14)
    self.ai_count = make_text((300, -250), size=14)
    self.player_card_t = make_text((-200, 50), size=16)
    self.ai_card_t = make_text((200, 50), size=16)

    self.next_btn = make_button("Play Round", (0, -320), self.next_round)
    self.diff_btn = make_button("Difficulty: medium", (0, -260), self.toggle_diff, width=3.2)
    write_text(self.info, "War - click Play Round")
    self.update_counts()

  def deal(self):
    self.player_pile.clear()
    self.ai_pile.clear()
    while self.deck:
      self.player_pile.append(self.deck.popleft())
      if self.deck:
        self.ai_pile.append(self.deck.popleft())

  def toggle_diff(self, *_):
    idx = DIFFICULTIES.index(self.difficulty)
    self.difficulty = DIFFICULTIES[(idx + 1) % len(DIFFICULTIES)]
    write_text(self.status, f"Difficulty set to {self.difficulty}")
    self.diff_btn.onclick(None)
    self.diff_btn = make_button(f"Difficulty: {self.difficulty}", (0, -260), self.toggle_diff, width=3.2)

  def order_winnings(self, cards: list[Card]) -> list[Card]:
    if self.difficulty == "easy":
      random.shuffle(cards)
      return cards
    if self.difficulty == "hard":
      return sorted(cards, key=lambda c: c.value, reverse=True)
    return cards

  def draw_for_war(self, pile: deque[Card], table: list[Card]) -> bool:
    if not pile:
      return False
    burn = min(3, len(pile) - 1) if len(pile) > 1 else 0
    for _ in range(burn):
      table.append(pile.popleft())
    if pile:
      table.append(pile.popleft())
      return True
    return False

  def play_round(self):
    if not self.player_pile or not self.ai_pile:
      return None
    table: list[Card] = []
    table.append(self.player_pile.popleft())
    table.append(self.ai_pile.popleft())
    while True:
      p_card, a_card = table[-2], table[-1]
      write_text(self.player_card_t, f"You: {p_card.label()}")
      write_text(self.ai_card_t, f"AI: {a_card.label()}")
      if p_card.value > a_card.value:
        self.player_pile.extend(table)
        return "player"
      if a_card.value > p_card.value:
        self.ai_pile.extend(self.order_winnings(table))
        return "ai"
      write_text(self.status, "WAR! Drawing extra cards...")
      if not self.draw_for_war(self.player_pile, table):
        return "ai"
      if not self.draw_for_war(self.ai_pile, table):
        return "player"

  def update_counts(self):
    write_text(self.player_count, f"Your pile: {len(self.player_pile)}")
    write_text(self.ai_count, f"AI pile: {len(self.ai_pile)}")

  def next_round(self, *_):
    if self.game_over:
      self.deck = deque(standard_deck())
      self.deal()
      self.round_no = 0
      self.game_over = False
      write_text(self.info, "New game - click Play Round")
      write_text(self.status, "")
      self.update_counts()
      return
    if not self.player_pile or not self.ai_pile:
      winner = "You win!" if len(self.player_pile) > len(self.ai_pile) else "AI wins!"
      write_text(self.info, winner)
      self.game_over = True
      write_text(self.status, "Click Play Round to restart.")
      return
    self.round_no += 1
    write_text(self.info, f"Round {self.round_no}")
    result = self.play_round()
    if result == "player":
      write_text(self.status, "You take the cards.")
    elif result == "ai":
      write_text(self.status, "AI takes the cards.")
    self.update_counts()
    if not self.player_pile or not self.ai_pile:
      winner = "You win the war!" if len(self.player_pile) > len(self.ai_pile) else "AI wins the war."
      write_text(self.info, winner)
      write_text(self.status, "Click Play Round to restart.")
      self.game_over = True


def main():
  WarUI()
  trtl.done()


if __name__ == "__main__":
  main()
