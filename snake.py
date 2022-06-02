import pygame as pg
from pygame.math import Vector2
from colors import COLORS

class Snake:

    ''' Class to store snake instances. The snake body is considered to be constituted by a set of squares (blocks)

    ATTRIBUTES:

        body :                  list containing the position of each individual block of the snake
        CELL_WIDTH :            length of an individual square of the grid
        block_size :            length of an individual block of the snake (with respect to CELL_WIDTH)
        direction :             current direction of the snake head
        new_direction :         next direction of the snake head (provided by the user)
        directions :            list of current directions for every snake's body piece7
        tail_direction :        a vector in the direction of the motion of the snake tail
        increase_body :         boolean to know whether increase the snake body or not
        new_block :             stores the position where to insert the new body block
        new_block_move :        boolean to know when to start moving new_block
        moves_wihout_eating :   the number of cells that snake has moved without eating
        is_virtual_snake :      a boolean to know whether the snake is virtual
        snake_color :           snake color
        cell_division :         number of steps needed to move from one square to another
        iterations :            number of steps taken from the last cell       
        EYES :                  image to display the snake eyes
        hit_sound :             game sound
        eating_sound :          game sound

    METHODS:

        draw_snake :                    displays the snake body using squares
        draw_intermediate_squares :     draws squares between the gaps of every block of the snake body
        move_snake :                    moves the snake body (and adds a new block when needed)
        body_block_directions :         computes the directions attribute 
    '''

    def __init__(self, color, cell_width, virtual_snake = False):

        self.body = [Vector2(5,4),Vector2(4,4),Vector2(3,4)]
        self.CELL_WIDTH = cell_width
        self.block_size = int(0.8 * self.CELL_WIDTH)

        self.direction = Vector2(0,0)
        self.new_direction = Vector2(0,0)
        self.directions = [0, 0 , 0]
        self.tail_direction = Vector2(1,0)

        self.increase_body = False
        self.new_block_move = False
        self.new_block = Vector2(0,0)
       
        self.moves_without_eating = 0
        self.is_virtual_snake = virtual_snake

        self.snake_color = color

        self.cell_division = 10
        self.iterations = 0

        self.EYES = pg.transform.scale(pg.transform.rotate(
            pg.image.load('images/snake_eyes.png'), 90), (0.8*self.CELL_WIDTH, 0.8*self.CELL_WIDTH))

        self.hit_sound = pg.mixer.Sound('sounds/hit.wav')
        self.eating_sound = pg.mixer.Sound('sounds/eating.wav')

    def draw_snake(self, WINDOW, coordinate_transform, args):

        #Displaying a square at the center of the cell (x, y) for
        # every 'block' in the snake body
        for i, body_block in enumerate(self.body):

            #x,y pixel position on the game board
            x = int(body_block.x * self.CELL_WIDTH  + 0.5 * (self.CELL_WIDTH - self.block_size))
            y = int(body_block.y * self.CELL_WIDTH + 0.5 * (self.CELL_WIDTH - self.block_size))

            x, y = coordinate_transform(x, y, args)
            body_rect = pg.Rect(x, y, self.block_size, self.block_size)
        
            pg.draw.rect(WINDOW, COLORS[self.snake_color], body_rect)

            if i != 0:
                
                #Filling the gaps between every square
                self.draw_intermediate_squares(WINDOW, i, 2, coordinate_transform, args)

        # x,y pixel position for the snake eyes (game board)   
        x_eyes = int(self.body[0].x * self.CELL_WIDTH  + 0.5 * (self.CELL_WIDTH - self.block_size))
        y_eyes = int(self.body[0].y * self.CELL_WIDTH + 0.5 * (self.CELL_WIDTH - self.block_size))

        x_eyes, y_eyes = coordinate_transform(x_eyes, y_eyes, args)

        eyes_rect = pg.Rect(x_eyes, y_eyes, self.CELL_WIDTH, self.CELL_WIDTH)

        #Rotating EYES image when necessary
        if self.direction.y != 0:
             WINDOW.blit(pg.transform.rotate(self.EYES, 90), eyes_rect)
            
        else:
            WINDOW.blit(self.EYES, eyes_rect)

    def draw_intermediate_squares(self, WINDOW, i, squares, coordinate_transform, args):

        '''
        Fills the gaps between squares of the snake body displaying squares

        i : index of the block in the snake body
        squares : number of squares to draw between the gap
        
        '''

        #x, y coordinate of the current block (i) and the next one (i-1)
        x_current = int(self.body[i].x * self.CELL_WIDTH  + 0.5 * (self.CELL_WIDTH - self.block_size))
        x_next = int(self.body[i-1].x * self.CELL_WIDTH  + 0.5 * (self.CELL_WIDTH - self.block_size))
        y_current = int(self.body[i].y * self.CELL_WIDTH + 0.5 * (self.CELL_WIDTH - self.block_size))
        y_next = int(self.body[i-1].y * self.CELL_WIDTH + 0.5 * (self.CELL_WIDTH - self.block_size))

        #Dividing the the line from (x_current, y_current) to (x_next, y_next)
        #into  equal segments
        for j in range(1, squares + 1):

            xj = j*x_current / (squares + 1) + (squares + 1 - j)*x_next / (squares + 1)
            yj = j*y_current / (squares + 1) + (squares + 1 - j)*y_next / (squares + 1)

            xj, yj = coordinate_transform(xj, yj, args)

            body_rect1 = pg.Rect(xj, yj, self.block_size, self.block_size)
            pg.draw.rect(WINDOW, COLORS[self.snake_color], body_rect1)

    
    def move_snake(self):

        '''
        Moves the body of the snake using self.directions
        If self.increase_body is True, add a new block
        

        EXTRA COMMENTS : the snake (head) can only move to a new direction when 
            it's located exactly at the centre of the cell. When the snake (head) is
            at the centre, we check for new directions.
            
            In order to make the motion
            more continuous we divide each cell into a number of divisions (self.cell_division) and we
            increase the position by 1/self.cell_division every iteration.
        '''
        #Snake (head) not at the centre of the cell

        if self.is_virtual_snake:
            if self.increase_body == True:
                body_copy = self.body[:]
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.increase_body = False

            else:
                tail_prev_pos = self.body[-1]
                body_copy = self.body[:-1]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]
                tail_new_pos = self.body[-1]
                self.tail_direction = tail_new_pos - tail_prev_pos

        else:
            if self.iterations < self.cell_division:
                for i in range(len(self.body)):
                    self.body[i] += self.directions[i] / self.cell_division

                self.iterations += 1

            #Snake (head) exactly at the centre of the cell
            else:

                #Checking if we have to increase the body
                if self.increase_body == True:
                    if self.new_block_move == True:
                        self.body.append(self.new_block)
                        self.increase_body = False
                        self.new_block_move = False

                    self.new_block_move = True

                self.direction = self.new_direction
                self.body_block_direction()
                self.iterations = 0
                self.move_snake()

    def body_block_direction(self):

        '''
        Used to compute self.directions
        '''

        directions = [0 for _ in range(len(self.body))]

        directions[0] = self.direction

        for i in range(1, len(self.body)):

            #Since the distance between every block is constant,
            #we can calculate the direction of motion as a subtraction
            directions[i] = self.body[i-1] - self.body[i]

        self.directions = directions


