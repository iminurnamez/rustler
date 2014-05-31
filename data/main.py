
from . import prepare,tools
from .states import game, titlescreen, storyscreen, worldmap, endscreen, controlsscreen

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"GAME": game.Game(),
                   "TITLE": titlescreen.TitleScreen(),
                   "STORY": storyscreen.StoryScreen(),
                   "CONTROLS": controlsscreen.ControlsScreen(),
                   "WORLDMAP": worldmap.WorldMap(),
                   "ENDSCREEN": endscreen.EndScreen()}
    controller.setup_states(states, "TITLE")
    controller.main()
