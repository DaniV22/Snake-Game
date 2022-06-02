### SNAKE GAME

The popular Snake game developed entirely in Python (OOP based), using PyGame library.

The game includes an options menu where one can customize to some extent the game, 
changing the size and color of the game board, the velocity and color of the snake and the number of fruits used in the game. There's an option
to use a pathfinding algorithm to let the snake moving by itself.

### About the Pathfinding algorithm

The Pathfinding algorithm uses the Breadth-First-Search (BFS) algorithm to find the shortest path between the snake head and the fruit.

The logic is as follows:

* If the snake follows the BFS-path to the fruit and there's an 'escape' path, follow this path.
* If not, the snake follows the longest path to its tail.
* If the longest path isn't available either, the snake goes to any 'safe' location.

This algorithm can lead to a dead end, especially when a fruit appears in front of the snake head right after the snake has eaten a fruit.

### Future implementations

* Increase the number of options available in the settings menu.
* Change the appearance of the snake, in order to make it look more realistic.
* Add new maps, with different shapes and obstacles.
* Train an AI to play the game.

