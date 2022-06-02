import pygame as pg

class Button():

    '''
    A class to create buttons that can be pressed by the user   

    ATTRIBUTES:

        image :             an image that represents the button
        rect :              rectangular area associated with the image
        rect.bottomleft :   position of the bottomleft corner of the rectangle
        clicked :           Boolean, to know if the buttons is clicked or not

    METHODS:

        set_pos : allows to set the bottomleft corner position of the rectangle
        draw : draws the button and check if it's been clicked

    '''

    def __init__(self, image):

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, 0)
        self.clicked = False

    def set_pos(self, x, y):

        self.rect.bottomleft = (x, y)

    def draw(self, window, clickable = True):

        '''
        Draws the button and checks if it's been clicked or not

        clickable : if True, the button can be clicked
        
        '''

        #draw button on screen
        window.blit(self.image, (self.rect.x, self.rect.y))

        #Checking if button can be clicked
        if clickable:

            #Mouse position
            pos = pg.mouse.get_pos()

            #Checking if mouse is over the button
            if self.rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True

            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return self.clicked
