from __future__ import unicode_literals # convenient for Python 2
import random
import sys
from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import *

from rdg import Maze

class font:
    SECTION_SIGN = u"\u00A7"
    PILCROW_SIGN = u"\u00B6"
    BULLET = u"\u2022"
    DOUBLE_EXCLAMATION_MARK = u"\u203C"
    LEFTWARDS_ARROW = u"\u2190"
    UPWARDS_ARROW = u"\u2191"
    RIGHTWARDS_ARROW = u"\u2192"
    DOWNWARDS_ARROW = u"\u2193"
    LEFT_RIGHT_ARROW = u"\u2194"
    UP_DOWN_ARROW = u"\u2195"
    UP_DOWN_ARROW_WITH_BASE = u"\u21A8"
    RIGHT_ANGLE = u"\u221F"
    #HOUSE = u"\u2302"
    HOUSE = u"\u2709"
    #BOX_DRAWINGS_DOUBLE_HORIZONTAL = u"\u2550"
    #BOX_DRAWINGS_DOUBLE_VERTICAL = u"\u2551"
    #BOX_DRAWINGS_DOUBLE_DOWN_AND_RIGHT = u"\u2554"
    #BOX_DRAWINGS_DOUBLE_DOWN_AND_LEFT = u"\u2557"
    #BOX_DRAWINGS_DOUBLE_UP_AND_RIGHT = u"\u255A"
    #BOX_DRAWINGS_DOUBLE_UP_AND_LEFT = u"\u255D"
    #BOX_DRAWINGS_DOUBLE_VERTICAL_AND_RIGHT = u"\u2560"
    #BOX_DRAWINGS_DOUBLE_VERTICAL_AND_LEFT = u"\u2563"
    #BOX_DRAWINGS_DOUBLE_DOWN_AND_HORIZONTAL = u"\u2566"
    #BOX_DRAWINGS_DOUBLE_UP_AND_HORIZONTAL = u"\u2569"
    #BOX_DRAWINGS_DOUBLE_VERTICAL_AND_HORIZONTAL = u"\u256C"


    BOX_DRAWINGS_DOUBLE_HORIZONTAL = u"\u2500"
    BOX_DRAWINGS_DOUBLE_VERTICAL = u"\u2502"
    BOX_DRAWINGS_DOUBLE_DOWN_AND_RIGHT = u"\u250c"
    BOX_DRAWINGS_DOUBLE_DOWN_AND_LEFT = u"\u2510"
    BOX_DRAWINGS_DOUBLE_UP_AND_RIGHT = u"\u2514"
    BOX_DRAWINGS_DOUBLE_UP_AND_LEFT = u"\u2518"
    BOX_DRAWINGS_DOUBLE_VERTICAL_AND_RIGHT = u"\u251c"
    BOX_DRAWINGS_DOUBLE_VERTICAL_AND_LEFT = u"\u2524"
    BOX_DRAWINGS_DOUBLE_DOWN_AND_HORIZONTAL = u"\u252c"
    BOX_DRAWINGS_DOUBLE_UP_AND_HORIZONTAL = u"\u2534"
    BOX_DRAWINGS_DOUBLE_VERTICAL_AND_HORIZONTAL = u"\u253c"

    BLACK_RECTANGLE = u"\u25AC"
    BLACK_UP_POINTING_TRIANGLE = u"\u25B2"
    BLACK_RIGHT_POINTING_POINTER = u"\u25BA"
    BLACK_DOWN_POINTING_TRIANGLE = u"\u25BC"
    BLACK_LEFT_POINTING_POINTER = u"\u25C4"
    WHITE_CIRCLE = u"\u25CB"
    INVERSE_BULLET = u"\u25D8"
    INVERSE_WHITE_CIRCLE = u"\u25D9"
    WHITE_SMILING_FACE = u"\u263A"
    BLACK_SMILING_FACE = u"\u263B"
    WHITE_SUN_WITH_RAYS = u"\u263C"
    FEMALE_SIGN = u"\u2640"
    MALE_SIGN = u"\u2642"
    BLACK_SPADE_SUIT = u"\u2660"
    BLACK_CLUB_SUIT = u"\u2663"
    BLACK_HEART_SUIT = u"\u2665"
    BLACK_DIAMOND_SUIT = u"\u2666"
    EIGHTH_NOTE = u"\u266A"
    BEAMED_EIGHTH_NOTES = u"\u266B"
    WHITE_RECT = u"\u2589"
    WHITE_SQR = u"\u2580"
    SMALL_WHITE_SQR = u"\u25a0"
    PATH_FULL = u"\u2593"
    TRIPLE_LINE = u"\u2261"
    UP_STAIRS = u"\u21f1"
    DOWN_STAIRS = u"\u21f2"
    POTION = u"\u00A1"
    GEAR = u"\u03a6"
    WEAPON = u"\u2320"
    SCROLL = u"\u003D"
    KEY = u"\u26b7"
    BONES = u"\u2620"
    COFFIN = u"\u26b0"
    TRAP = u"\u2623"
    MOB = u"\u2639"
    COIN = u"\u26c0" # 26c1
    EMPTY = u"\u0000"
    ARROW = u"\u27b3"


    BOLD = '\033[1m'
    ENDC = '\033[0m'




class Game(object):

    def __init__(self):
        self.menu_width = 30
        self.maze = Maze(width=25, height=17)
        self.menu_active = True
        self.input = None
        self.selected_menu = 'Main Menu'
        self.selected = 0
        self.previous_menus = []
        self._run()

    def _handleInput(self):
        self.a[0, 40:40+len(self.input)] = [self.input]

        if self.menu_active:
            self._mainMenu()
        return True

    def _mainMenu(self):
        if self.input == '<UP>':
            self._selection(-1)
            self._drawMainMenu()
        if self.input == '<DOWN>':
            self._selection(1)
            self._drawMainMenu()
        if self.input == '<Ctrl-j>':
            choice = self.menu[self.selected_menu].keys()[self.selected]
            self.menu[self.selected_menu][choice]()
            self.selected_menu = choice
            self._refreshScreen()

        if self.input == '<ESC>' or self.input == '<BACKSPACE>':
            self._exit()



    def _drawMainMenu(self):
        self.menu = {
            'Main Menu': {'Start Game': self._refreshScreen, 'Exit Game': self._exit},
            'Start Game': {'Empty': None, 'Nothing': None}
        }

        # Border
        if not self.selected_menu == 'Main Menu':
            for y in range(self.window.height - (self.window.height / 3)):
                y += self.window.height / 3
                if y == self.window.height - 1:
                    self.a[y, 0] = font.BOX_DRAWINGS_DOUBLE_UP_AND_RIGHT
                    # Middle of the line
                    for x in range(self.menu_width - 1):
                        self.a[y, x + 1] = font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    # End of the line
                    self.a[y, self.menu_width] = font.BOX_DRAWINGS_DOUBLE_UP_AND_LEFT
                else:
                    self.a[y, 0] = font.BOX_DRAWINGS_DOUBLE_VERTICAL
                    self.a[y, self.menu_width] = font.BOX_DRAWINGS_DOUBLE_VERTICAL

        # Title
        title = '- {} -'.format(self.selected_menu)
        middle = (self.menu_width / 2) - (len(title) / 2)

        self.a[self.window.height / 3 + 1, middle:middle+len(self.selected_menu)] = [yellow(bold(self.selected_menu))]

        # Choices
        for i, item in enumerate(self.menu[self.selected_menu].keys()):
            y = self.window.height / 3 + 3
            item = '- ' + item
            if self.selected == i:
                self.a[y + i, 2:2+len(item)] = [bold(item)]
            else:
                self.a[y + i, 2:2+len(item)] = [item]

    def _selection(self, dir):
        if self.selected + dir < 0:
            self.selected = len(self.menu[self.selected_menu]) - 1
        elif self.selected + dir > len(self.menu[self.selected_menu]) - 1:
            self.selected = 0
        else:
            self.selected += dir


    def _refreshScreen(self):
        self.a = FSArray(self.window.height, self.window.width)
        self._drawStatus()
        self._drawMaze()
        self._drawMainMenu()


    def _exit(self):
        sys.exit(0)


    def _drawStatus(self):
        for y in range(self.window.height / 3):
            # Border
            # Top Line
            if y ==0:
                # Begining of the line
                self.a[y, 0] = font.BOX_DRAWINGS_DOUBLE_DOWN_AND_RIGHT
                # Middle of the line
                for x in range(self.menu_width - 1):
                    self.a[y, x + 1] = font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                # End of the line
                self.a[y, self.menu_width] = font.BOX_DRAWINGS_DOUBLE_DOWN_AND_LEFT
            # Bottom line
            elif y == (self.window.height / 3) - 1:
                # Begining of the line
                self.a[y, 0] = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_RIGHT
                # Middle of the line
                for x in range(self.menu_width - 1):
                    self.a[y, x + 1] = font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                # End of the line
                self.a[y, self.menu_width] = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_LEFT
            else:
                self.a[y, 0] = font.BOX_DRAWINGS_DOUBLE_VERTICAL
                self.a[y, self.menu_width] = font.BOX_DRAWINGS_DOUBLE_VERTICAL

            # Details
            # Draw Player Name
            if y == 1:
                name = '-Player Name-'
                x = (self.menu_width /2) - (len(name) / 2)
                self.a[y, x:x+len(name)] = (name,)

            # Draw Health
            if y == 3:
                full_health = 230.0
                health = 100.0
                health_width = 10

                health_bad = '-' * (int(health_width - health / full_health * health_width) + (health % full_health > 0))
                health_good = font.WHITE_SQR * int(health / full_health * health_width)
                health_text = ' [{}]'.format(health_good + health_bad)
                alt_health_text = 'HP: ' + str(int(health)) + ' / ' + str(int(full_health)) + health_text
                self.a[y, 2:2+len(alt_health_text)] = (red(alt_health_text),)
                #self.a[y + 1, 2:2+len(health_text)] = (red(health_text),)

            # Draw mana
            if y == 4:
                full_mana = 230.0
                mana = 150.0
                mana_width = 10
                mana_bad = '-' * (int(mana_width - mana / full_mana * mana_width) + (mana % full_mana > 0))
                mana_good = font.WHITE_SQR * int(mana / full_mana * mana_width)
                mana_text = '[{}]'.format(mana_good + mana_bad)
                #alt_mana_text = 'MP: ' + str(int(mana)) + ' / ' + str(int(full_mana)) + mana_text
                alt_mana_text = 'MP: {} / {} {}'.format(int(mana), int(full_mana), mana_text)
                self.a[y, 2:2+len(alt_mana_text)] = (blue(alt_mana_text),)


    def _translate(self,y, x, col):
        #        up dn lt rt
        walls = [0, 0, 0, 0]
        #         ul ur dl dr
        kiddie = [0, 0, 0, 0]
        if self.maze.getMazeCell(int(y) - 1, int(x), 1) in [2, 3, 4, 6]:
            walls[0] = 1
        if self.maze.getMazeCell(int(y) + 1, int(x), 1) in [2, 3, 4, 6]:
            walls[1] = 1
        if self.maze.getMazeCell(int(y), int(x) - 1, 1) in [2, 3, 4, 6]:
            walls[2] = 1
        if self.maze.getMazeCell(int(y), int(x) + 1, 1) in [2, 3, 4, 6]:
            walls[3] = 1

        if self.maze.getMazeCell(int(y) - 1, int(x) - 1, 1) in [2, 3, 4, 6]:
            kiddie[0] = 1
        if self.maze.getMazeCell(int(y) - 1, int(x) + 1, 1) in [2, 3, 4, 6]:
            kiddie[1] = 1
        if self.maze.getMazeCell(int(y) + 1, int(x) - 1, 1) in [2, 3, 4, 6]:
            kiddie[2] = 1
        if self.maze.getMazeCell(int(y) + 1, int(x) + 1, 1) in [2, 3, 4, 6]:
            kiddie[3] = 1

        tile = None
        # Floor Translating
        if col[1] == 1:
           tile = green(font.BULLET + ' ')
           tile = green('. ')

        # Wall Translating
        if col[1] == 2:
            # Check for 4 way
            if walls.count(1) == 4:
                if kiddie.count(1) < 4:
                    if kiddie.count(1) <= 1:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    # 3 Kiddies
                    if kiddie == [0, 1, 1, 1]:
                        tile = font.BOX_DRAWINGS_DOUBLE_UP_AND_LEFT + ' '
                    if kiddie == [1, 0, 1, 1]:
                        tile = font.BOX_DRAWINGS_DOUBLE_UP_AND_RIGHT + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    if kiddie == [1, 1, 0, 1]:
                        tile = font.BOX_DRAWINGS_DOUBLE_DOWN_AND_LEFT + ' '
                    if kiddie == [1, 1, 1, 0]:
                        tile = font.BOX_DRAWINGS_DOUBLE_DOWN_AND_RIGHT + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL

                    # 2 Kiddies
                    if kiddie == [1, 1, 0, 0]:
                        tile = font.BOX_DRAWINGS_DOUBLE_DOWN_AND_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    if kiddie == [1, 0, 1, 0]:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_RIGHT + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    if kiddie == [1, 0, 0, 1]:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    if kiddie == [0, 1, 0, 1]:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_LEFT + ' '
                    if kiddie == [0, 0, 1, 1]:
                        tile = font.BOX_DRAWINGS_DOUBLE_UP_AND_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    if kiddie == [0, 1, 1, 0]:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                else:
                    tile = '  '

            # Check for 3 way
            elif walls.count(1) == 3:
                #            up dn lt rt
                if walls == [1, 1, 1, 0]:
                    if kiddie[0] == 1 and kiddie[2] == 1:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL + ' '
                    else:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_LEFT + ' '
                if walls == [1, 1, 0, 1]:
                    if kiddie[1] == 1 and kiddie[3] == 1:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL + ' '
                    else:
                        tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL_AND_RIGHT + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                if walls == [1, 0, 1, 1]:
                    if kiddie[0] == 1 and kiddie[1] == 1:
                        tile = font.BOX_DRAWINGS_DOUBLE_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    else:
                        tile = font.BOX_DRAWINGS_DOUBLE_UP_AND_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                if walls == [0, 1, 1, 1]:
                    if kiddie[2] == 1 and kiddie[3] == 1:
                        tile = font.BOX_DRAWINGS_DOUBLE_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                    else:
                        tile = font.BOX_DRAWINGS_DOUBLE_DOWN_AND_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL

            # Check for 2 way
            elif walls.count(1) == 2:
                if walls == [1, 0, 1, 0]:
                    tile = font.BOX_DRAWINGS_DOUBLE_UP_AND_LEFT + ' '
                if walls == [1, 0, 0, 1]:
                    tile = font.BOX_DRAWINGS_DOUBLE_UP_AND_RIGHT + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                if walls == [0, 1, 1, 0]:
                    tile = font.BOX_DRAWINGS_DOUBLE_DOWN_AND_LEFT + ' '
                if walls == [0, 1, 0, 1]:
                    tile = font.BOX_DRAWINGS_DOUBLE_DOWN_AND_RIGHT + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                if walls == [0, 0, 1, 1]:
                    tile = font.BOX_DRAWINGS_DOUBLE_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL
                if walls == [1, 1, 0, 0]:
                    tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL + ' '


            # Check for single
            elif walls.count(1) == 1:
                if walls == [1, 0, 0, 0]:
                    tile = font.BOX_DRAWINGS_DOUBLE_VERTICAL + ' '
                if walls == [0, 1, 0, 0]:
                    tile = '  '
                if walls == [0, 0, 1, 0]:
                    tile = font.BOX_DRAWINGS_DOUBLE_HORIZONTAL + ' '
                if walls == [0, 0, 0, 1]:
                    tile = font.BOX_DRAWINGS_DOUBLE_HORIZONTAL + font.BOX_DRAWINGS_DOUBLE_HORIZONTAL

            # Check for none
            elif walls.count(1) == 0:
                tile =  font.SMALL_WHITE_SQR + ' '

            tile = blue(tile)

        # Translating Locked Door
        if col[1] == 3:
            if walls[0] == 1 and walls[1] == 1:
                tile = red(font.INVERSE_WHITE_CIRCLE + ' ')
            else:
                tile = red(font.INVERSE_WHITE_CIRCLE) + blue(font.BOX_DRAWINGS_DOUBLE_HORIZONTAL)

        # Translating Unlocked Door
        if col[1] == 4:
            if walls[0] == 1 and walls[1] == 1:
                tile = green(font.INVERSE_WHITE_CIRCLE + ' ')
            else:
                tile = green(font.INVERSE_WHITE_CIRCLE) + blue(font.BOX_DRAWINGS_DOUBLE_HORIZONTAL)

        # Translating Chest
        if col[1] == 5:
            tile = yellow(font.HOUSE + ' ')

        # Translating Secret Door
        if col[1] == 6:
            if walls[0] == 1 and walls[1] == 1:
                tile = magenta(font.INVERSE_WHITE_CIRCLE + ' ')
            else:
                tile = magenta(font.INVERSE_WHITE_CIRCLE) + blue(font.BOX_DRAWINGS_DOUBLE_HORIZONTAL)

        # Translating Trap
        if col[1] == 7:
            tile = red(font.TRAP + ' ')

        # Translating Mob
        if col[1] == 8:
            tile = cyan(font.MOB + ' ')

        # Translating Up Stairs
        if col[1] == 9:
            tile = blue(font.UP_STAIRS + ' ')

        # Translating Down Stairs
        if col[1] == 10:
            tile = blue(font.DOWN_STAIRS + ' ')

        # Translating Gold
        if col[1] == 20:
            tile = yellow(font.WHITE_SUN_WITH_RAYS + ' ')

        # Translating Potion
        if col[1] == 21:
            tile = yellow(font.POTION + ' ')

        # Translating Gear
        if col[1] == 22:
            tile = yellow(font.GEAR + ' ')

        # Translating Weapon
        if col[1] == 23:
            tile = yellow(font.WEAPON + ' ')

        # Translating Scroll
        if col[1] == 24:
            tile = yellow(font.SCROLL + ' ')

        # Translating Key
        if col[1] == 25:
            tile = yellow(font.KEY + ' ')

        # Translating Bones
        if col[1] == 26:
            tile = yellow(font.BONES + ' ')
        try:
            return bold(tile)
        except:
            import pdb; pdb.set_trace()


    def _drawMaze(self):

        for i in sorted(self.maze.maze.iterkeys(), key=int):
          for x in sorted(self.maze.maze[i].iterkeys(), key=int):
            col = self.maze.getMazeCell(i, x)
            tile = self._translate(i, x, col)

            middle_x = ((self.window.width - self.menu_width) / 2) + (self.maze.width / 2)
            middle_y = (self.window.height / 2) - (self.maze.height / 2)

            #num_x = int(x) * len(tile) + middle_x
            #num_y = int(i) + middle_y

            #self.a[num_y, num_x:num_x+len(tile)] = (tile,)

            num_x = int(x) * len(tile) + self.menu_width + 1
            num_y = int(i)
            self.a[num_y, num_x:num_x+len(tile)] = (tile,)


    def _run(self):
        with FullscreenWindow() as self.window:
            self.a = FSArray(self.window.height, self.window.width)
            self._drawMainMenu()
            self.window.render_to_terminal(self.a)
            with Input() as self.input_generator:
                for c in self.input_generator:
                    self.input = c
                    result = self._handleInput()
                    if not result:
                        break
                    self.window.render_to_terminal(self.a)


def main():
    g = Game()


if __name__ == '__main__':
    main()