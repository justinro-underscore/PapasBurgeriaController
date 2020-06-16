#
# If can't connect to display ":0": b'No protocol specified\n'
# Run `xhost +`
#

import pyautogui
import cv2
import os
import sys
from getch import getch
from states import papasBurgeriaStates, State, MouseEvent, MouseEventType, get_relative_coords

# https://www.coolmathgames.com/0-papas-burgeria

class Box:
  def __init__(self, left, top, width, height):
    self.left = left
    self.top = top
    self.width = width
    self.height = height

class Runner:

  def __init__(self):
    self.run()

  def __pull_screen_pos(self):
    gamePos = pyautogui.locateOnScreen("PapasTitle.png", confidence=0.9)
    if gamePos:
      return gamePos
    else:
      raise RuntimeError("Could not find Papa's Burgeria Title")

  def on_keystroke(self, keystroke):
    mouse_event = None
    if keystroke in list(map(str, range(10))):
      mouse_event = self.curr_state.num_events[int(keystroke) - 1]
    elif self.curr_state.add_events and keystroke in self.curr_state.add_events:
      mouse_event = self.curr_state.add_events[keystroke]

    if mouse_event:
      if mouse_event.type == MouseEventType.SINGLE:
        coords = get_relative_coords(self.screen_pos, mouse_event.coords)
        pyautogui.click(x=coords[0], y=coords[1])
      elif mouse_event.type == MouseEventType.DRAG:
        start_coords = get_relative_coords(self.screen_pos, mouse_event.coords[0])
        end_coords = get_relative_coords(self.screen_pos, mouse_event.coords[1])
        pyautogui.moveTo(start_coords[0], start_coords[1])
        pyautogui.dragTo(end_coords[0], end_coords[1], 0.2, button='left')
      elif mouse_event.type == MouseEventType.DOUBLE:
        raise RuntimeError("Not implemented")
      elif mouse_event.type == MouseEventType.MULTIPLE:
        raise RuntimeError("Not implemented")

      os.system("wmctrl -a Terminal")
      new_state = None
      if mouse_event.next_state:
        new_state = mouse_event.next_state
      elif mouse_event.post_func:
        new_state = mouse_event.post_func(self.screen_pos)

      if new_state:
        if new_state in papasBurgeriaStates:
          self.curr_state = papasBurgeriaStates[new_state]
        else:
          raise RuntimeError("State {" + new_state + "} either doesn't exist or is not in defined states")
      self.curr_state.print_events()


  def run(self):
    try:
      if len(sys.argv) > 1:
        if len(sys.argv) > 2:
          self.screen_pos = Box(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        else:
          default_box = Box(564, 349, 641, 482)
          self.screen_pos = default_box

        if sys.argv[1] in papasBurgeriaStates:
          self.curr_state = papasBurgeriaStates[sys.argv[1]]
        else:
          raise RuntimeError("Debug state not found")
      else:
        self.screen_pos = self.__pull_screen_pos()
        self.curr_state = papasBurgeriaStates["title_screen"]
      print("Game found! Begin input")
      self.curr_state.print_events()
      keystroke = getch()
      while keystroke != "0":
        self.on_keystroke(keystroke)
        keystroke = getch()
      print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
      print("Returning control to the system")
    except RuntimeError as e:
      print("ERROR: " + str(e))

Runner()