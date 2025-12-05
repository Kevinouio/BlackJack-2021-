import random
import turtle as trtl
from collections import defaultdict

DIFFICULTIES = ("easy", "medium", "hard")


class MemoryAI:
  def __init__(self, difficulty: str):
    self.difficulty = difficulty
    self.known: dict[str, set[int]] = defaultdict(set)

  def remember(self, idx: int, value: str):
    self.known[value].add(idx)

  def forget_randomly(self):
    # medium forgets half of its knowledge periodically
    for key in list(self.known.keys()):
      if random.random() < 0.5:
        self.known.pop(key, None)

  def pick(self, tiles: list[str], found: set[int]) -> tuple[int, int]:
    unknown = [i for i in range(len(tiles)) if i not in found]
    if self.difficulty == "easy":
      return random.sample(unknown, 2)

    if self.difficulty == "medium":
      if random.random() < 0.5:
        self.forget_randomly()
      for val, idxs in self.known.items():
        unseen = [i for i in idxs if i not in found]
        if len(unseen) >= 2:
          return unseen[0], unseen[1]
      for val, idxs in self.known.items():
        unseen = [i for i in idxs if i not in found]
        if unseen:
          other = random.choice([i for i in unknown if i != unseen[0]])
          return unseen[0], other
      return random.sample(unknown, 2)

    for val, idxs in self.known.items():
      unseen = [i for i in idxs if i not in found]
      if len(unseen) >= 2:
        return unseen[0], unseen[1]
    singles = [(v, list(idxs)[0]) for v, idxs in self.known.items() if len(idxs) == 1 and list(idxs)[0] not in found]
    if singles:
      _, idx_one = singles[0]
      other = random.choice([i for i in unknown if i != idx_one])
      return idx_one, other
    return random.sample(unknown, 2)


def build_board(size: int = 4) -> list[str]:
  pairs = [chr(ord("A") + i) for i in range((size * size) // 2)]
  tiles = pairs * 2
  random.shuffle(tiles)
  return tiles


# UI section
from ui_common import setup_screen, register_common_shapes, make_button, make_text, write_text  # noqa: E402


class MemoryGameUI:
  def __init__(self):
    self.wn = setup_screen("Memory")
    register_common_shapes()
    self.difficulty = "medium"
    self.tiles: list[str] = []
    self.found: set[int] = set()
    self.player_score = 0
    self.ai_score = 0
    self.ai = MemoryAI(self.difficulty)
    self.player_turn = True
    self.game_over = False

    self.info = make_text((0, 320), size=18)
    self.status = make_text((0, 280), size=14)
    self.board_text = make_text((0, 120), size=12)
    self.score_text = make_text((0, -260), size=14)
    self.next_btn = make_button("Play Turn", (0, -320), self.play_turn)
    self.diff_btn = make_button("Difficulty: medium", (0, -260), self.toggle_diff, width=3.2)

    self.reset_game()

  def toggle_diff(self, *_):
    idx = DIFFICULTIES.index(self.difficulty)
    self.difficulty = DIFFICULTIES[(idx + 1) % len(DIFFICULTIES)]
    self.ai.difficulty = self.difficulty
    write_text(self.status, f"Difficulty set to {self.difficulty}")
    self.diff_btn.onclick(None)
    self.diff_btn = make_button(f"Difficulty: {self.difficulty}", (0, -260), self.toggle_diff, width=3.2)

  def reset_game(self):
    self.tiles = build_board()
    self.found = set()
    self.player_score = 0
    self.ai_score = 0
    self.ai = MemoryAI(self.difficulty)
    self.player_turn = True
    self.game_over = False
    write_text(self.info, "Memory - your turn")
    self.update_board()
    self.update_scores()

  def update_board(self, show: tuple[int, int] | None = None):
    lines = []
    for i, val in enumerate(self.tiles):
      if i in self.found or (show and i in show):
        cell = val
      else:
        cell = f"{i+1:02}"
      lines.append(cell)
    grid = []
    for r in range(4):
      grid.append(" ".join(lines[r * 4:(r + 1) * 4]))
    write_text(self.board_text, "\n".join(grid))

  def update_scores(self):
    write_text(self.score_text, f"Scores — You: {self.player_score} | AI: {self.ai_score}")

  def prompt_player_choice(self) -> tuple[int, int] | None:
    prompt = "Pick two tiles (1-16) separated by space or comma:"
    user = self.wn.textinput("Your move", prompt)
    if not user:
      return None
    parts = []
    for sep in (",", " "):
      if sep in user:
        parts = [p for p in user.split(sep) if p.strip()]
        break
    if not parts:
      parts = [user]
    if len(parts) != 2:
      write_text(self.status, "Enter exactly two numbers.")
      return None
    try:
      a, b = int(parts[0]) - 1, int(parts[1]) - 1
    except ValueError:
      write_text(self.status, "Numbers only.")
      return None
    if a == b or not (0 <= a < len(self.tiles)) or not (0 <= b < len(self.tiles)):
      write_text(self.status, "Invalid positions.")
      return None
    if a in self.found or b in self.found:
      write_text(self.status, "Tile already matched.")
      return None
    return a, b

  def player_turn_logic(self):
    picks = self.prompt_player_choice()
    if not picks:
      return
    a, b = picks
    self.update_board((a, b))
    write_text(self.status, f"You flipped {self.tiles[a]} and {self.tiles[b]}.")
    if self.tiles[a] == self.tiles[b]:
      self.found.update([a, b])
      self.player_score += 1
      self.update_scores()
      self.update_board()
      write_text(self.status, "Match! You go again.")
      return
    self.player_turn = False
    self.update_board()

  def ai_turn_logic(self):
    a, b = self.ai.pick(self.tiles, self.found)
    self.ai.remember(a, self.tiles[a])
    self.ai.remember(b, self.tiles[b])
    self.update_board((a, b))
    write_text(self.status, f"AI flips {a+1} and {b+1}: {self.tiles[a]} / {self.tiles[b]}")
    if self.tiles[a] == self.tiles[b]:
      self.found.update([a, b])
      self.ai_score += 1
      self.update_scores()
      self.update_board()
      write_text(self.status, "AI found a match and goes again.")
      return
    self.player_turn = True
    self.update_board()

  def check_end(self) -> bool:
    if len(self.found) == len(self.tiles):
      if self.player_score > self.ai_score:
        write_text(self.info, "You win Memory!")
      elif self.ai_score > self.player_score:
        write_text(self.info, "AI wins Memory.")
      else:
        write_text(self.info, "Memory ends in a tie.")
      write_text(self.status, "Click Play Turn to restart.")
      self.game_over = True
      return True
    return False

  def play_turn(self, *_):
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
  MemoryGameUI()
  trtl.done()


if __name__ == "__main__":
  main()
