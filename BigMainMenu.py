#This Main Menu should be the default screen of both the game and the interactive map 
#When idle, this screen will show. It will have the same controls as the game itself,
#So the up and down and left and right arrow keys will move the paw indicator over the buttons.
#Their will be four buttons consisting of "Map", "Game", "About", and "Credits"
#The Map and Game buttons will be side by side, and the about and credits buttons
#will be stacked on top of each other below and in the middle of the two bigger buttons.

import pygame
#Using import os so that it can take the images out of the assets folder
import os

pygame.init()


#Setting the screen display width and heights
height = 900 
width = 1200
screen = pygame.display.set_mode((width,height))

#Importing and sizing background
background = pygame.image.load("menu_background.jpg")
background = pygame.transform.scale(background,(width,height))

#Importing and sizing buttons
gamebutton = pygame.image.load("Game_Button.png")
gamebutton = pygame.transform.scale(gamebutton,(int(width/3),int(height/5)))
mapbutton = pygame.image.load("Map_Button.png")
mapbutton = pygame.transform.scale(mapbutton,(int(width/3),int(height/5)))
# settingsbutton = pygame.image.load("settings_button.jpg")
# settingsbutton = pygame.transform.scale(settingsbutton,(int(width/5),int(height/9)))
aboutbutton = pygame.image.load("about_button.jpg")
aboutbutton = pygame.transform.scale(aboutbutton,(int(width/5),int(height/9)))

#Importing and scaling the paw indicator used for BigMainMenu and the Game
indicator = pygame.image.load("indicator_paw.png")
indicator = pygame.transform.scale(indicator,(int(height/12),int(height/12)))

# Positions for indicator: to the bottom of top two buttons, and to the right of bottom two buttons
positionslist = [(int(3*width/12.5),int(height/2.25)),(int(3*width/4.25),int(height/2.25)),
                 (int(7*width/11),int(7*height/12))]
position = 2 # Current position, indicated by place in positionslist

def drawscreen():
    screen.blit(background, (0,0))
    screen.blit(gamebutton,(int(width/1.75),int(height/4)))
    screen.blit(mapbutton, (int(width/11.75),int(height/4)))
    screen.blit(aboutbutton,(int(5*width/12),int(7*height/12)))
    screen.blit(indicator,positionslist[position])
    pygame.display.update()

drawscreen()

runningmenu = True


while runningmenu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button selected, end
            runningmenu = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and position == 1:
                position -=1
                drawscreen()
            elif event.key == pygame.K_RIGHT and position == 0:
                position += 1
                drawscreen()
        elif event.type == pygame.KEYDOWN: # For keys up and down, move
            if event.key == pygame.K_UP and position > 0: # indicator.
                position -= 1
                drawscreen()
            elif event.key == pygame.K_DOWN and position < 2:
                position += 1
                drawscreen()
            elif event.key == pygame.K_DOWN and position == 2:
                position = 0
                drawscreen()
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if position == 0:
                    #open interactive map
                    import InteractiveMap.SpeciesMenu
                    import InteractiveMap.Species_Bison
                    import InteractiveMap.Bison_Identification
                    import InteractiveMap.BisonText
                    import InteractiveMap.Species_GrayFox
                    import InteractiveMap.Species_GrayWolf
                    import InteractiveMap.Species_RedFox
                    import InteractiveMap.Species_Turtle
                elif position == 1:
                    import main
                    # Launch game!
                else:
                    # Open settings
                    import BigAbout # Reads the file
                    BigAbout.about_screen(screen)
                    drawscreen()