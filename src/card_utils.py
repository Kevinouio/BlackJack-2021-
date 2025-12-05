from dataclasses import dataclass
import random
from typing import List

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
SUITS = ["hearts", "diamonds", "clubs", "spades"]
RANK_VALUES = {rank: idx + 2 for idx, rank in enumerate(RANKS)}


@dataclass(frozen=True)
class Card:
  rank: str
  suit: str
  value: int

  def label(self) -> str:
    return f"{self.rank} of {self.suit}"


def standard_deck(shuffle: bool = True) -> List[Card]:
  """Create a standard 52-card deck."""
  deck = [Card(rank=r, suit=s, value=RANK_VALUES[r]) for s in SUITS for r in RANKS]
  if shuffle:
    random.shuffle(deck)
  return deck


def format_hand(hand: List[Card]) -> str:
  return ", ".join(card.label() for card in hand)
