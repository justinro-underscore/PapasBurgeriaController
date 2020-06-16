#
# If can't connect to display ":0": b'No protocol specified\n'
# Run `xhost +`
#

import pyautogui
import cv2
import os
from getch import getch
from states import papasBurgeriaStates, State, MouseEvent, MouseEventType

# https://www.coolmathgames.com/0-papas-burgeria

class Runner:

  def __init__(self):
    self.run()

  def __pull_screen_pos(self):
    gamePos = pyautogui.locateOnScreen("PapasTitle.png", confidence=0.9)
    if gamePos:
      return gamePos
    else:
      raise RuntimeError("Could not find Papa's Burgeria Title")
  
  def __get_relative_coords(self, coords):
    x_factor = MouseEvent.coords_ref_frame[0] / self.screen_pos.width
    y_factor = MouseEvent.coords_ref_frame[1] / self.screen_pos.height
    return [(coords[0] * x_factor) + self.screen_pos.left, (coords[1] * y_factor) + self.screen_pos.top]

  def on_keystroke(self, keystroke):
    mouse_event = None
    if keystroke in list(map(str, range(10))):
      mouse_event = self.curr_state.num_events[int(keystroke) - 1]
    elif self.curr_state.add_events and keystroke in self.curr_state.add_events:
      mouse_event = self.curr_state.add_events[keystroke]

    if mouse_event:
      if mouse_event.type == MouseEventType.SINGLE:
        coords = self.__get_relative_coords(mouse_event.coords)
        pyautogui.click(x=coords[0], y=coords[1])
      elif mouse_event.type == MouseEventType.DRAG:
        start_coords = self.__get_relative_coords(mouse_event.coords[0])
        end_coords = self.__get_relative_coords(mouse_event.coords[1])
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
      elif mouse_event.check_state:
        new_state = mouse_event.check_state()

      if new_state:
        if new_state in papasBurgeriaStates:
          self.curr_state = papasBurgeriaStates[new_state]
        else:
          raise RuntimeError("State {" + new_state + "} either doesn't exist or is not in defined states")
      self.curr_state.print_events()


  def run(self):
    try:
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