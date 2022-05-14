'''
Function to transform gameboard coordinates to pygame WINDOW coordinates

ARGUMENTS:

    x : x-coordinate in gameboard frame
    y : y-coordinate in gameboard frame
    args :  a list of constants

RETURN :    x, y coordinates in the pygame WINDOW frame
'''

def coordinate_transform(x, y, args):

    window_size, x_squares, y_squares, square_width = args

    #Just a translation
    delta_x = (window_size - x_squares*square_width) / 2
    delta_y = (window_size + 50 - y_squares*square_width) / 2

    x += delta_x
    y += delta_y

    return x, y 