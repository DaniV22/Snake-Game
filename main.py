import pygame as pg
from pygame.math import Vector2

from game import Game

#Initializing all pygame modules
pg.init()

#Size of the window
WINDOW_SIZE = 750

#Creating a Window
WINDOW = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pg.display.set_caption('Snake game')

#Creating a clock to control the game FPS
clock = pg.time.Clock()

#MAIN function
def main():

    #Default options (Speed, Size, Nº Fruits, Map color, Snake color, Autopilot)
    default = ['NORMAL', 'MEDIUM', 'ONE', 'GREEN_MAP', 'RED', 'NO']

    #Creating game object
    game = Game(WINDOW, default)

    #Main game
    while True:

        game.settings.settings_button.set_pos(0.92*WINDOW_SIZE, 60)

        #FPS of the game 
        #(also used as the velocity of the game)
        velocity = game.game_variables[0]

        #Increasing the game velocity when using autopilot
        if game.autopilot:
            velocity += 80

        clock.tick(velocity)

        #If the snake is not moving, user can
        # change the settings
        if game.snake.direction == (0,0):
            click_settings = game.settings.settings_button.draw(WINDOW)
            pg.time.delay(50)

        #Close game  
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break

            #Next direction of the snake (head)
            #Snake can't move in the opposite direction 
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT and game.snake.direction.x != 1:
                    game.snake.new_direction = Vector2(-1, 0)

                if event.key == pg.K_RIGHT and game.snake.direction.x != -1:
                    game.snake.new_direction = Vector2(1,0)

                if event.key == pg.K_UP and game.snake.direction.y != 1 :
                    game.snake.new_direction = Vector2(0, -1)

                if event.key == pg.K_DOWN and game.snake.direction.y != -1:
                    game.snake.new_direction = Vector2(0,1)

        if game.playing == True: 
            #Checking if the snake x,y-position are integers
            # so the snake can move to a new direction
            if (abs(game.snake.body[0][0] - round(game.snake.body[0][0])) < 0.001) and (
                abs(game.snake.body[0][1] - round(game.snake.body[0][1])) < 0.001):

                #Rounding the coordinates of the snake body to avoid
                # decimal errors
                for i in range(len(game.snake.body)):
                    game.snake.body[i] = Vector2(round(game.snake.body[i][0]), round(game.snake.body[i][1]))

                #Autopilot case
                if game.autopilot:
                
                    #Creating the path using the pathfinder
                    path = game.pathfinder.get_path(game.snake, game.fruit)

                    if path:

                        #Directions to move the snake to the neighbor location
                        x_dir = path[0][0] - game.snake.body[0][0]
                        y_dir = path[0][1] - game.snake.body[0][1]

                    game.snake.new_direction = Vector2(x_dir, y_dir)

                game.snake.direction = game.snake.new_direction
                game.snake.body_block_direction()
          
            #SETTINGS WINDOW

            #If user click in the settings button
            if click_settings:
                game.display_settings = True

            #If user clicked once, we display the menu
            if game.display_settings == True:
                game.draw_window()

                #Changing game options
                if game.settings.check_option(WINDOW):
                    game.display_settings = False
                    default = game.settings.get_options()
                    game = Game(WINDOW, default)

            #Settings window closed
            else:
                game.update()
                game.draw_window()
                game.snake.moves_without_eating += 1 / game.snake.cell_division

            pg.display.update()

        #Not playing (ending)
        else:
            game.draw_window()
            play_again, exit = game.ending()
            pg.time.delay(100)

            if play_again:

                #Changing the Autopilot option to prevent the game
                # from playing indefinitely
                default[-1] = 'NO'
                game = Game(WINDOW, default)

            elif exit:
                break
            

if __name__ == '__main__':
    main()