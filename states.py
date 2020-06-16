import pyautogui
import enum
from time import sleep

class MouseEventType(enum.Enum):
  SINGLE = 1
  DRAG = 2
  DOUBLE = 3
  MULTIPLE = 4

class MouseEvent:
  coords_ref_frame = [642, 481] # Defines size of window all coords are based on

  def __init__(self, name, event_type, coords, next_state=None, check_state=None):
    self.name = name
    self.type = event_type
    self.coords = coords
    self.check_state = check_state
    self.next_state = next_state

class State:
  def __init__(self, num_events, add_events=None):
    if len(num_events) > 9:
      raise ValueError("Too many events!")
    self.num_events = [None] * 9
    for i, event in enumerate(num_events):
      self.num_events[i] = event
    self.add_events = add_events
  
  def print_events(self):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for i, event in enumerate(self.num_events):
      if event:
        print(str(i + 1) + ": " + event.name)
      else:
        break
    if self.add_events:
      for key, event in self.add_events.items():
        print(key + ": " + event.name)

def check_for_existing_save():
  select = pyautogui.locateOnScreen("PapasSelectCharacter.png", confidence=0.9)
  if select:
    return "player_select"
  else:
    return "save_screen"

papasBurgeriaStates = {
  "title_screen": State([
    MouseEvent("Start", MouseEventType.SINGLE, [326, 331], next_state="select_save")
  ]),
  "select_save": State([
    MouseEvent("Save 1", MouseEventType.SINGLE, [120, 411], check_state=check_for_existing_save),
    MouseEvent("Save 2", MouseEventType.SINGLE, [318, 411], check_state=check_for_existing_save),
    MouseEvent("Save 3", MouseEventType.SINGLE, [531, 411], check_state=check_for_existing_save),
  ]),
  "player_select": State([
    MouseEvent("Marty", MouseEventType.SINGLE, [232, 385], next_state="cutscene"),
    MouseEvent("Rita", MouseEventType.SINGLE, [416, 385], next_state="cutscene"),
  ]),
  "save_screen": State([
    MouseEvent("Upgrade Shop", MouseEventType.SINGLE, [258, 381], next_state="upgrade_shop"),
    MouseEvent("Continue", MouseEventType.SINGLE, [383, 381], next_state="order_station"),
  ]),
  "cutscene": State([
    MouseEvent("Skip", MouseEventType.SINGLE, [575, 446], next_state="order_station"),
  ]),
  "cutscene": State([
    MouseEvent("Skip", MouseEventType.SINGLE, [575, 446], next_state="order_station"),
  ]),
  "order_station": State([
    MouseEvent("Order Station", MouseEventType.SINGLE, [219, 455], next_state="order_station"),
    MouseEvent("Grill Station", MouseEventType.SINGLE, [327, 455], next_state="grill_station"),
    MouseEvent("Build Station", MouseEventType.SINGLE, [426, 455], next_state="build_station"),
  ]),
  "grill_station": State([
    MouseEvent("Order Station", MouseEventType.SINGLE, [219, 455], next_state="order_station"),
    MouseEvent("Grill Station", MouseEventType.SINGLE, [327, 455], next_state="grill_station"),
    MouseEvent("Build Station", MouseEventType.SINGLE, [426, 455], next_state="build_station"),
  ]),
  "build_station": State([
    MouseEvent("Order Station", MouseEventType.SINGLE, [219, 455], next_state="order_station"),
    MouseEvent("Grill Station", MouseEventType.SINGLE, [327, 455], next_state="grill_station"),
    MouseEvent("Build Station", MouseEventType.SINGLE, [426, 455], next_state="build_station"),
  ],
  add_events={
    "B": MouseEvent("Top Bun", MouseEventType.DRAG, [[58, 114], [324, 75]]),
    "t": MouseEvent("Tomato", MouseEventType.DRAG, [[58, 161], [324, 75]]),
    "l": MouseEvent("Lettuce", MouseEventType.DRAG, [[58, 213], [324, 75]]),
    "o": MouseEvent("Onion", MouseEventType.DRAG, [[58, 261], [324, 75]]),
    "p": MouseEvent("Pickle", MouseEventType.DRAG, [[58, 304], [324, 75]]),
    "P": MouseEvent("Patty", MouseEventType.DRAG, [[190, 400], [324, 75]]),
    "c": MouseEvent("Cheese", MouseEventType.DRAG, [[58, 353], [324, 75]]),
    "b": MouseEvent("Bottom Bun", MouseEventType.DRAG, [[58, 398], [324, 75]]),
    "k": MouseEvent("Ketchup", MouseEventType.DRAG, [[446, 373], [324, 75]]),
    "m": MouseEvent("Mustard", MouseEventType.DRAG, [[500, 373], [324, 75]]),
    "M": MouseEvent("Mayo", MouseEventType.DRAG, [[553, 373], [324, 75]]),
    "q": MouseEvent("BBQ", MouseEventType.DRAG, [[605, 373], [324, 75]]),
  }),
}