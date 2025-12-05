from pathlib import Path
import turtle as trtl

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR.parent / "assets"
CARDS_DIR = ASSETS_DIR / "cards"
UI_DIR = ASSETS_DIR / "ui"


def setup_screen(title: str = "Card Game") -> trtl.Screen:
  wn = trtl.Screen()
  wn.title(title)
  wn.setup(width=1000, height=800)
  background = UI_DIR / "Playing_card_Background.gif"
  if background.exists():
    wn.bgpic(str(background))
  return wn


def register_common_shapes():
  wn = trtl.Screen()
  back = CARDS_DIR / "Back_of_playing_card.gif"
  for shape in [back, UI_DIR / "play_again.gif", UI_DIR / "rules.gif", UI_DIR / "stand.gif", UI_DIR / "hit.gif"]:
    if shape.exists():
      wn.addshape(str(shape))


def make_button(text: str, position: tuple[float, float], callback, width: float = 2.5, height: float = 1.0) -> trtl.Turtle:
  btn = trtl.Turtle()
  btn.hideturtle()
  btn.penup()
  btn.shape("square")
  btn.color("white")
  btn.shapesize(stretch_wid=height, stretch_len=width)
  btn.goto(position)
  btn.showturtle()
  label = trtl.Turtle(visible=False)
  label.penup()
  label.color("black")
  label.goto(position[0], position[1] - 10)
  label.write(text, align="center", font=("Verdana", 14, "bold"))
  btn.onclick(callback)
  return btn


def make_text(position: tuple[float, float], color: str = "white", align: str = "center", size: int = 16) -> trtl.Turtle:
  t = trtl.Turtle(visible=False)
  t.penup()
  t.color(color)
  t.goto(position)
  t._font = ("Verdana", size, "bold")
  return t


def write_text(turtle_obj: trtl.Turtle, message: str):
  turtle_obj.clear()
  turtle_obj.write(message, align="center", font=turtle_obj._font)
