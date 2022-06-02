from snake import Snake
from pygame.math import Vector2
from random import shuffle

class Pathfinder:

    '''
    Class to compute the path that snake must follow to eat a 
    piece of fruit 

    ATTRIBUTES:

        CELL_WIDTH :    size of a single cell of the game board
        x_squares :     number of cells in the game board in x-direction
        y_squares :     number of cells in the game board in y-direction
        CELLS :         list containing every cell coordinate in the game board

    METHODS:

        manhattan_distance :       computes the Manhattan distance (aka Taxicab) between two points
        is_empty_cell :            returns False if a specific cell is occupied and True otherwise
        get_free_neighbors :       returns free neighbors of a specific position
        create_virtual_snake :     creates a copy of the original snake
        path_to_tail :             creates a path between the head of the snake and its tail
        breadth_search_first :     creates the shortest path between two points using the BFS algorithm
        longest_path_to_tail :     creates the longest path between the head of the snake and its tail
        safe_move :                creates a path to any 'safe' location
        get_path :                 creates the 'final' path depending on every possible case
    '''

    def __init__(self, x_squares, y_squares, CELL_WIDTH):

        self.CELL_WIDTH = CELL_WIDTH
        self.x_squares = x_squares
        self.y_squares = y_squares
        self.CELLS = [[i, j] for i in range(self.x_squares) for j in range(self.y_squares)]

    def manhattan_distance(self, pos1, pos2):
        '''
        Computes the Manhattan distance between two points (pos1 and pos2)
        It's the sum of the absolute difference between the x and y positions
        '''

        x1, y1 = pos1
        x2, y2 = pos2

        return abs(x2 - x1) + abs(y2 - y1)

    def is_empty_cell(self, current_pos, snk_body):

        '''
        Checks if the position (current_pos) is available or not
        
        '''
        #Current pos out of the game board
        if (current_pos[0] >= self.x_squares or current_pos[0] < 0) or (
            current_pos[1] >= self.y_squares or current_pos[1] < 0):

            return False

        #Position occupied by the snake body
        for block_pos in snk_body:
            if block_pos == current_pos:
                return False

        return True

    def get_free_neighbors(self, current_pos, snk_body, fruit_pos):

        '''
        Gets every free neighbor of a specific location
        '''

        #Every neighbor of the current location
        neighbors = [[current_pos[0] + 1, current_pos[1]], [current_pos[0] - 1, current_pos[1]],
                 [current_pos[0], current_pos[1] + 1], [current_pos[0], current_pos[1] - 1]]

        free_neighbors = []

        for neighbor in neighbors:
            #If the neighbor is free, we add it to free_neighbors
            if self.is_empty_cell(neighbor, snk_body) and fruit_pos != neighbor:
                free_neighbors.append(tuple(neighbor))

        return free_neighbors

    def create_virtual_snake(self, snake):

        '''
        Creates a copy of the snake. We only need to copy the parameters associated
        with the motion of the virtual snake
        '''

        snake_copy = Snake(snake.snake_color, self.CELL_WIDTH, True)
        snake_copy.body  = snake.body[:]
        snake_copy.direction = snake.direction

        return snake_copy

    def path_to_tail(self, snake):

        #Path from the head of the snake to its tail
        path = self.breadth_first_search(tuple(snake.body[0]), tuple(snake.body[-1]), snake.body[:-1])

        return path


    def breadth_first_search(self, start_pos, end_pos, snake_body):

        #Initializing visited positions and parents nodes
        visited = {tuple(pos): False for pos in self.CELLS}
        parent_nodes = {tuple(pos): None for pos in self.CELLS}

        #Initial Queue and visited position
        queue = [start_pos]  
        visited[start_pos] = True

        #All neighbors for every cell in the game board
        all_neighbors = {tuple(pos): [[pos[0] + 1, pos[1]], [pos[0] - 1, pos[1]],
                 [pos[0], pos[1] + 1], [pos[0], pos[1] - 1]] for pos in self.CELLS}

        # While queue is not empty
        while queue:

            node = queue.pop(0)
            current_neighbors = all_neighbors[node]
            
            #Iterating through every neighbor of the current node
            for next_node in current_neighbors:

                #Checking if the cell is free and is not visited
                if self.is_empty_cell(next_node, snake_body) and not visited[tuple(next_node)]:
                    queue.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    parent_nodes[tuple(next_node)] = node


        #Reconstructing the path
        path = list()
        parent_node = end_pos

        while True:

            #There's no path
            if parent_nodes[tuple(parent_node)] is None:
                return []

            #New parent node
            parent_node = parent_nodes[tuple(parent_node)]

            #If we arrive at the starting position, we've finished
            if parent_node == start_pos:
                path.append(end_pos)

                return path

            #Constructing the path
            path.insert(0, parent_node)
    
    def longest_path_to_tail(self, snake, fruit):

        '''
         Creates the longest path between the head of the snake and its tail
         '''

        #Neighbors of the current location (head)
        neighbors = self.get_free_neighbors(snake.body[0], snake.body, fruit.positions[0])
        path = []

        if neighbors:

            distance = -1      #Default value

            #Iterating thorugh every neighbor
            for neighbor in neighbors:

                #Checking if the distance between the neighbor and
                # the tail increases
                if self.manhattan_distance(neighbor, snake.body[-1]) > distance:

                    #Creating a virtual snake
                    v_snake = self.create_virtual_snake(snake)

                    #Directions to move the snake to the neighbor location
                    x_dir = neighbor[0] - v_snake.body[0][0]
                    y_dir = neighbor[1] - v_snake.body[0][1]
                    v_snake.direction = Vector2(x_dir, y_dir)
                  
                    #Moving virtual snake
                    v_snake.move_snake()

                    #Checking if the virtual snake eats a fruit
                    if v_snake.body[0] == fruit.positions[0]:
                        new_block = v_snake.body[-1] - v_snake.tail_direction
                        v_snake.body.append(new_block)

                    #If the snake can follow its tail in the new
                    # location, we add it into the path
                    if self.path_to_tail(v_snake):
                        path.append(neighbor)
                        distance = self.manhattan_distance(neighbor,snake.body[-1])

            #Returning the path (if exists) wich
            # maximize the distance        
            if path:
                return [path[-1]]

    def safe_move(self, snake, fruit):

        #Available neighbors of the current location
        neighbors = self.get_free_neighbors(snake.body[0], snake.body[:-1], fruit.positions[0])

        #Shuffling the neighbors to avoid cycles
        shuffle(neighbors)

        paths = []
        if neighbors:

            #Iterating through every neighbor
            for neighbor in neighbors:

                #Adding the neighbor into the path
                paths.append(neighbor)

                #Creating a virtual snake
                v_snake = self.create_virtual_snake(snake)

                #Directions to move the snake to the neighbor location
                x_dir = paths[-1][0] - v_snake.body[0][0]
                y_dir = paths[-1][1] - v_snake.body[0][1]

                v_snake.direction = Vector2(x_dir, y_dir)

                #Moving the virtual snake
                v_snake.move_snake()

                #If the snake can follow its tail in the new
                # location, we add it into the path
                if self.path_to_tail(v_snake):
                    return [paths[-1]]

                #Else, the snake follows its tail
                else:
                    return self.path_to_tail(snake)

    def get_path(self, snake, fruit):

        '''
        Creates the 'final' path depending on every possible case.

        '''

        #To prevent the snake from moving in cycles at the end
        if snake.moves_without_eating >= 10*self.x_squares*self.y_squares and (
            self.manhattan_distance(snake.body[0], fruit.positions[0]) == 1):

            return [fruit.positions[0]]

        #Creating a virtual snake
        v_snake = self.create_virtual_snake(snake)

        #Shortest path to the fruit
        path_to_fruit = self.breadth_first_search(tuple(v_snake.body[0]), tuple(fruit.positions[0]), v_snake.body)

        path_to_tail = []

        if path_to_fruit:

            #Making the virtual snake to follow the path
            # to the fruit
            for pos in path_to_fruit:

                #Directions to move the snake to the neighbor location
                x_dir = pos[0] - v_snake.body[0][0]
                y_dir = pos[1] - v_snake.body[0][1]

                v_snake.direction = Vector2(x_dir, y_dir)

                #Moving the virtual snake
                v_snake.move_snake()

            #Increasing the size of the virtual snake, because
            # it eat a fruit
            new_block = v_snake.body[-1] - v_snake.tail_direction
            v_snake.body.append(new_block)

            #Path from the snake head to its tail
            # from the fruit position
            path_to_tail = self.path_to_tail(v_snake)
        
        #If there's an 'escape' path (path_to_tail)
        # the real snake will follow the path_to_fruit
        if path_to_tail:
            return path_to_fruit

        # If path_to_fruit or path_to_tail are not available:
        # ------We make the snake follow the longest path to its tail
        # ------If it's not available either, we make the snake follow a 'safe_move'

        #Longest path to snake tail
        longest_path = self.longest_path_to_tail(snake, fruit)

        if longest_path:
            return longest_path

        #Safe move
        safe_move = self.safe_move(snake, fruit)

        if safe_move:
            return safe_move


    
