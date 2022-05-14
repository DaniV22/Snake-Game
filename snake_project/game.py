import pygame as pg
from pygame.math import Vector2
import itertools

from snake import Snake
from fruit import Fruit
from button import Button
from dimmer import Dimmer
from settings import Settings

from coord_transform import coordinate_transform
from colors import COLORS

game_font = pg.font.SysFont('comicsans', 45)

game_variables = {'FAST' : 85, 'NORMAL': 65, 'SLOW': 50,
 'BIG': [19, 17], 'MEDIUM': [12, 11], 'SMALL': [8, 8],
  'THREE': 3, 'TWO': 2, 'ONE': 1,
   'RED_MAP': ['RED', 'WHITE'], 'GREEN_MAP': ['GREEN', 'DARK_GREEN'], 'BLUE_MAP': ['BLUE', 'LIGHT_BLUE'],
   'YELLOW': 'YELLOW', 'RED': 'RED', 'BLUE': 'BLUE'}

class Game:

    '''
    A class that handles every game event

    ATTRIBUTES:

        game_variables : a list of the option values chosen by the user (or default)
        WINDOW : the window in which the game is displayed
        WINDOW_SIZE : the size (pixels) of the self.WINDOW object
        X_SQUARES, Y_SQUARES : number of squares in the game board in the X and Y directions
        _ IMAGES : some images in the game
        snake : Snake object
        fruit : Fruit object
            fruit.new_pos : sets up a random position for the fruit(s)
        
        play_again_object : a button object associated with PLAY_AGAIN_IMAGE
        exit_button : a button object associated with the EXIT_IMAGE
        settings : a Settings object
        dim : a dimmer object
        playing : boolean to know if the game continues or not
        display_settings : boolean to know if displaying the settings or not
        victory : a sound played when you win the game

    METHODS:

        draw_window : calls every drawing method7
        draw_grid : draws a grid of a specific color and size
        fruit_collision : handles the collisions with the fruits (a.k.a eating)
        snake_dead : checks if the snake collides with the borders or itself
        game_won : checks if the player's got the max. score
        ending : displays a little menu to know if playing again or ending the game
        update : updates every game event and dynamics
        draw_score : draws the current score of the player

    '''

    def __init__(self, WINDOW, variables):

        self.game_variables = [game_variables[variable] for variable in variables]
        self.WINDOW = WINDOW
        self.WINDOW_SIZE = 750
        self.X_SQUARES, self.Y_SQUARES = self.game_variables[1]
        self.CELL_WIDTH = max(int(self.WINDOW_SIZE / (self.X_SQUARES + 1)),int(
            (self.WINDOW_SIZE - 50) /(self.Y_SQUARES + 1)))

        self.SCORE_IMAGE = pg.transform.scale(pg.image.load('images/food_image.png'), (55, 55))
        self.PLAY_AGAIN_IMAGE = pg.transform.scale(pg.image.load('images/play_again.png'), (150, 90))
        self.EXIT_IMAGE = pg.transform.scale(pg.image.load('images/exit.png'), (165, 100))
        self.SETTINGS_IMAGE = pg.transform.scale(pg.image.load('images/settings.png'), (60, 60))

        self.snake = Snake(self.game_variables[4], self.CELL_WIDTH)
        self.fruit = Fruit(self.game_variables[2], self.CELL_WIDTH)
        self.fruit.new_pos(self.snake.body, self.X_SQUARES, self.Y_SQUARES)

        self.play_again_button = Button(self.PLAY_AGAIN_IMAGE)
        self.exit_button = Button(self.EXIT_IMAGE)
        self.settings = Settings()

        self.dim = Dimmer(keepalive=1)
        self.playing = True
        self.display_settings = False

        self.victory = pg.mixer.Sound('sounds/victory.wav')

    def draw_window(self):

        '''
        Calls all the drawing methods
        '''

        #Constants to compute the coordinate transformation
        args = [self.WINDOW_SIZE, self.X_SQUARES, self.Y_SQUARES, self.CELL_WIDTH]

        self.draw_grid()
        self.fruit.draw_fruit(self.WINDOW,self.CELL_WIDTH, coordinate_transform, args)
        self.snake.draw_snake(self.WINDOW, coordinate_transform, args)
        self.draw_score(20, 0)
        self.settings.settings_button.draw(self.WINDOW, False)

    def draw_grid(self):

        #Constants to compute the coordinate transformation
        args = [self.WINDOW_SIZE, self.X_SQUARES, self.Y_SQUARES, self.CELL_WIDTH]

        #Background
        self.WINDOW.fill(COLORS['DARK_GREY'])
        upper_rect = pg.Rect(0, 0, self.WINDOW_SIZE, 50)
        pg.draw.rect(self.WINDOW, COLORS['LIGHT_GREY'], upper_rect)

        #Colors of the grid
        grid_color =  itertools.cycle((
            COLORS[self.game_variables[3][0]], COLORS[self.game_variables[3][1]]))

        #Creating the grid
        for i in range(0, self.X_SQUARES*self.CELL_WIDTH, self.CELL_WIDTH):
            for j in range(0, self.Y_SQUARES*self.CELL_WIDTH, self.CELL_WIDTH):
                xi, yj = coordinate_transform(i, j, args)
                rect = pg.Rect(xi, yj, self.CELL_WIDTH, self.CELL_WIDTH)
                pg.draw.rect(self.WINDOW, next(grid_color), rect)    #Alternating between the 2 colors

            if self.Y_SQUARES % 2 == 0:
                next(grid_color)

    def fruit_collision(self):

        '''
        Checks if the snake collides with a fruit (snake eats a fruit)
        
        '''

        #Iterating through every fruit
        for i, pos in enumerate(self.fruit.positions):

            #If both positions coincide, the snake
            #has eaten the fruit and so we incrase its length
            if self.snake.body[0] == pos:
                self.snake.new_block = Vector2(self.snake.body[-1]) #Storing position of the tail
                self.fruit.remove_fruit(i)
                self.snake.increase_body = True
                self.snake.eating_sound.play()
                self.fruit.new_pos(self.snake.body, self.X_SQUARES, self.Y_SQUARES)

    def snake_dead(self):

        dead = False

        #Checking if the snake is collides with borders
        if not -0.3 < round(self.snake.body[0].x, 3) < self.X_SQUARES - 0.7 or not -0.3 < round(
            self.snake.body[0].y, 3) < self.Y_SQUARES - 0.7:
            dead = True

        #Checking if the snake is collides with its body
        for body_block in self.snake.body[1:]:
            if body_block == self.snake.body[0]:
                dead = True

        if dead:
            self.snake.hit_sound.play()
            pg.time.delay(2000)
            self.playing = False

    def game_won(self):

        #There are no places to add more fruits, so
        # player has obtained max score
        if self.fruit.number_of_fruits == 0:
            self.victory.play()
            pg.time.delay(3000)
            self.playing = False

    def ending(self):
        '''
        Displays a little self.WINDOW to know if playing again or ending the game. 
        Also shows the score obtainded by the player

        '''

        args = [self.WINDOW_SIZE, self.X_SQUARES, self.Y_SQUARES, self.CELL_WIDTH]

        #Darkening the background self.WINDOW
        self.dim.dim()

        #Setting the position and size of the self.WINDOW
        WIDTH, HEIGHT = self.X_SQUARES*self.CELL_WIDTH, self.Y_SQUARES*self.CELL_WIDTH
        center = coordinate_transform(WIDTH/2, 0.8*HEIGHT/2, args)
        rect = pg.Rect(0, 0, WIDTH/ 2.1, HEIGHT / 3)
        rect.center = (center)
        pg.draw.rect(self.WINDOW, COLORS['LIGHT_GREY'], rect)

        #Position of the score obtained
        x_score = rect.topleft[0] + 10
        y_score = rect.topleft[1] + 5
        score_surface = game_font.render('SCORE: ', 1, COLORS['BLACK'])
        self.WINDOW.blit(score_surface, (x_score, y_score))

        #Score
        self.draw_score(x_score + 180, y_score)

        #Play again button
        self.play_again_button.set_pos(
            rect.bottomleft[0] +  10, rect.bottomleft[1] - 10)

        #Exit button
        self.exit_button.set_pos(
            rect.midbottom[0] , rect.midbottom[1] - 10)

        #Waiting for the player to click
        play_again = self.play_again_button.draw(self.WINDOW)
        exit = self.exit_button.draw(self.WINDOW)

        pg.display.update()

        return play_again, exit

    def update(self):

        #Waiting until the snake moves
        if self.snake.direction != (0,0):

            self.snake.move_snake()
            self.fruit_collision()
            self.snake_dead()
            self.game_won()

    def draw_score(self, x, y):

        '''
        Draws the current score of the player. Also used at the end of the game

            x, y : position in which to display the score

        '''
        #Score text (fruits eaten)
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, 1, COLORS['BLACK'])
        self.WINDOW.blit(score_surface, (x + 60, y - 3))

        #Score image (fruit image)
        score_rect = pg.Rect(x, y, 60, 60)
        self.WINDOW.blit(self.SCORE_IMAGE, score_rect)