'''
There are 5 variables, with 3 options each one, that can be changed by the user:

    Snake_vel : the velocity of the snake
    Map_size : the size of the map
    Fruit_num : number of fruits to use in the game
    Map_color : color palette of the map
    Snake_color : color of the snake
'''

import pygame as pg
from button import Button
from colors import COLORS

pg.init()
settings_font = pg.font.SysFont('comicsans', 45)
pathfinder_font = pg.font.SysFont('comicsans', 30)

class Settings:

    '''
    A class to display a settings menu which allows user to
    change some options in the game

    ATTRIBUTES:

        x :                    width of the menu
        y :                    height of the menu
        rect :                 a rectangle object associated to the menu to store rectangular coordinates
        SETTINGS_IMAGE :       image representing the settings menu
        CLOSE_IMAGE :          image of an X mark
        PATHFINDER_IMAGE :     image of a robot
        close_button :         button object associated with CLOSE_IMAGE
        PATHFINDER_button :    button object associated with PATHFINDER_IMAGE
        settings_button :      button object associated with SETTINGS_IMAGE
        option_rects :         a list to store the rectangle objects associated with the options
        clicked :              a list to store the options that have been clicked

    METHODS:

        draw_menu :         draws all the menu
        draw_lines :        draws lines around a rect. object
        draw_sep_lines :    draws lines separating the differents options
        draw_options :      displays an image associated with every option
        check_options :     calls draw_menu and cheks which options have been clicked
        get_options :       returns a list of the clicked options

    '''

    def __init__(self):

        self.x = 500
        self.y = 480
        self.rect = pg.Rect(100, 100, self.x, self.y)
        self.SETTINGS_IMAGE = pg.transform.scale(pg.image.load('images/settings.png'), (60, 60))
        self.CLOSE_IMAGE = pg.transform.scale(pg.image.load('images/settings_images/CLOSE.png'), (35, 35))
        self.PATHFINDER_IMAGE = pg.transform.scale(pg.image.load('images/settings_images/pathfinder.png'), (26, 26))
        self.close_button = Button(self.CLOSE_IMAGE)
        self.pathfinder_button = Button(self.PATHFINDER_IMAGE)
        self.settings_button = Button(self.SETTINGS_IMAGE)
        self.option_rects = []
        self.clicked = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1]

    def draw_menu(self, WINDOW):
        pg.draw.rect(WINDOW, COLORS['LIGHT_BLUE'], self.rect)
        self.draw_lines(WINDOW, self.rect, 'BLACK')
        self.draw_sep_lines(WINDOW)
        self.draw_options(WINDOW)

    def draw_lines(self, WINDOW, rect, color):

        pg.draw.line(WINDOW, COLORS[color], rect.topleft, rect.bottomleft, 4)
        pg.draw.line(WINDOW, COLORS[color], rect.topright, rect.bottomright, 4)
        pg.draw.line(WINDOW, COLORS[color], rect.topleft, rect.topright, 4)
        pg.draw.line(WINDOW, COLORS[color], rect.bottomright, rect.bottomleft, 4)

    def draw_sep_lines(self, WINDOW):

        '''
        Draws lines separating the variables
        
        '''

        #Separations between two consecutive lines
        separation = (self.rect.bottom - self.rect.top - 40)/ 5

        for i in range(5):

            pg.draw.line(WINDOW, COLORS['BLACK'], (self.rect.left, self.rect.top + 45 + i*separation),
             (self.rect.right, self.rect.top + 45 + i*separation), 4)
    
    def draw_options(self, WINDOW):

        #Variables and their possible values
        options = {'Snake Vel.': ['FAST', 'NORMAL', 'SLOW'], 
        'Map Size': ['BIG', 'MEDIUM', 'SMALL'], 'Fruit Num.': ['THREE', 'TWO', 'ONE'],
        'Map Color': ['RED_MAP', 'GREEN_MAP', 'BLUE_MAP'], 'Snake Color': ['YELLOW', 'RED', 'BLUE']}

        for i, key in enumerate(options):

            #Separations between two consecutives variables
            separation = (self.rect.bottom - self.rect.top - 40) / 5

            #Displaying the name of the different variables
            x_option = self.rect.left + 10
            y_option = self.rect.top + 50 + i*separation
            option_surface = settings_font.render(f'{key}', 1, COLORS['BLACK'])
            WINDOW.blit(option_surface, (x_option, y_option))

            #Iterating through the different values of every variables
            for j, option in enumerate(options[key]):

                option_sep = 70  #Separation between every option

                #Rectangle associated with the option
                rect_ij = pg.Rect(self.rect.right - option_sep*(j + 1), y_option + 10, 55, 55)
                pg.draw.rect(WINDOW, COLORS['WHITE'], rect_ij)
                self.option_rects.append(rect_ij)

                #Image associated with the option
                OPTION_IMAGE = pg.transform.scale(pg.image.load(f'images/settings_images/{option}.png'), (55, 55))

                option_rect = pg.Rect(rect_ij.x, rect_ij.y, 55, 55)
                WINDOW.blit(OPTION_IMAGE, option_rect)


    def check_option(self, WINDOW):

        '''
        Calls draw_menu and cheks which options have been clicked        
        '''

        #Drawing the menu
        self.option_rects = []
        self.draw_menu(WINDOW)

        #Drawing the close button
        self.close_button.set_pos(self.rect.topright[0] - 42, self.rect.top + 40)
        close_options = self.close_button.draw(WINDOW)

        #Drawing the pathfinder button
        pathfinder_surface = pathfinder_font.render('Pathfinder', 1, COLORS['BLACK'])
        WINDOW.blit(pathfinder_surface, (self.rect.left + 10, self.rect.top - 2))
        pathfinder_rect = pg.Rect(self.rect.left + 170, self.rect.top - 30 + 35, 35, 35)
        self.pathfinder_button.set_pos(pathfinder_rect.left + 5, self.rect.top + 35)
        pathdfinder_option = self.pathfinder_button.draw(WINDOW)

        if self.clicked[-2]:
            self.draw_lines(WINDOW, pathfinder_rect, 'BLACK')
        
        else:
            self.draw_lines(WINDOW, pathfinder_rect, 'LIGHT_GREY')

        pos = pg.mouse.get_pos()    #Mouse position

        #Iterating through every option
        for i, option in enumerate(self.option_rects):

            #Checking if mouse is over the button
            if option.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1:
                    self.clicked[i] = 1

                    #We make sure only an option for each variable
                    #can be clicked
                    if i % 3 == 0:
                        self.clicked[i + 1], self.clicked[i + 2] = 0, 0
                    
                    elif i % 3 == 1:
                        self.clicked[i - 1], self.clicked[i + 1] = 0, 0

                    else:
                        self.clicked[i - 2], self.clicked[i - 1] = 0, 0
                    
            #Highlighting the clicked option
            if self.clicked[i]:
                self.draw_lines(WINDOW, option, 'BLACK')

            else:
                self.draw_lines(WINDOW, option, 'LIGHT_GREY')

        if pathdfinder_option:
            self.clicked[-1], self.clicked[-2] = self.clicked[-2], self.clicked[-1]

        if close_options:
            return True

        else:
            return False


    def get_options(self):

        '''
        Returns a list of the clicked options: option if clicked == 1

        The options must be in the correct order!
        '''

        options = ['FAST', 'NORMAL', 'SLOW', 'BIG', 'MEDIUM', 'SMALL',
        'THREE', 'TWO', 'ONE', 'RED_MAP', 'GREEN_MAP', 'BLUE_MAP', 
        'YELLOW', 'RED', 'BLUE', 'YES', 'NO']

        return [option for i, option in enumerate(options) if self.clicked[i] == 1]


                    
                    
