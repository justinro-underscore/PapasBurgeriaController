import pyautogui
import enum
from time import sleep

class MouseEventType(enum.Enum):
  SINGLE = 1
  DOUBLE = 2
  MULTIPLE = 3

class MouseEvent:
  coords_ref_frame = [642, 481] # Defines size of window all coords are based on

  def __init__(self, name, event_type, coords, next_state=None, check_state=None):
    self.name = name
    self.type = event_type
    self.coords = coords
    self.check_state = check_state
    self.next_state = next_state

class State:
  def __init__(self, events):
    if len(events) > 9:
      raise ValueError("Too many functions!")
    self.events = [None] * 9
    for i, event in enumerate(events):
      self.events[i] = event
  
  def print_events(self):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for i, event in enumerate(self.events):
      if event:
        print(str(i + 1) + ": " + event.name)
      else:
        return

def check_for_existing_save():
  sleep(0.5)
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
    MouseEvent("Continue", MouseEventType.SINGLE, [383, 381], next_state="main_game"),
  ]),
  "cutscene": State([
    MouseEvent("Skip", MouseEventType.SINGLE, [575, 446], next_state="main_game"),
  ]),
}