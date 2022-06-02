import pygame as pg
from random import sample, choice

class Fruit:

    ''' Class to store fruit instances

    ATTRIBUTES :

        number_of_fruit :   number of pieces of fruit used in the game
        positions :         a list storing the positions of every fruit
        fruit_image :       an image of a fruit

    METHODS : 

        draw_fruit :    displays every fruit at their corresponding position
        new_pos :       calculates a new (possible) random position for the food
        remove_fruit :  removes the fruit at a corresponding index
    '''

    def __init__(self, num_fruits, CELL_WIDTH):

        self.number_of_fruits = num_fruits
        self.positions = []

        self.fruit_IMAGE = fruit_IMAGE = pg.transform.scale(
            pg.image.load('images/food_image.png'), (CELL_WIDTH, CELL_WIDTH))

    def draw_fruit(self, WINDOW, CELL_WIDTH, coordinate_transform, args):

        ''' Displaying fruit(s) at its (their) corresponding location

        '''

        for pos in self.positions:

            #Transforming a list of integers numbers (x, y location in the game board reference)
            # into pixel location (general Window reference)
            x, y = coordinate_transform(int(pos[0] * CELL_WIDTH), int(pos[1] * CELL_WIDTH), args)

            fruit_rect = pg.Rect(x, y, CELL_WIDTH, CELL_WIDTH)
            WINDOW.blit(self.fruit_IMAGE, fruit_rect)


    def new_pos(self, snake_body, X_SQUARES, Y_SQUARES):

        #List of all positions on the game board
        all_positions = [[i, j] for i in range(X_SQUARES) for j in range(Y_SQUARES)]

        #Removing the positions occupied by the snake body
        for body_block in snake_body:

            all_positions.remove(body_block)

        #Used only at the beggining of the game
        if len(self.positions) == 0 and len(snake_body) < 4:
            self.positions = sample(all_positions, self.number_of_fruits)

        else:
            #Removing the positions occupied by other fruits
            for fruit_pos in self.positions:
                all_positions.remove(fruit_pos)

            #If there are no possible positions, we don't
            # add more fruit
            if len(all_positions) == 0:
                self.number_of_fruits -= 1

            else:
                self.positions.append(choice(all_positions))
    
    def remove_fruit(self, index):

        #Remove the fruit at 'index' positions
        self.positions.pop(index)






    