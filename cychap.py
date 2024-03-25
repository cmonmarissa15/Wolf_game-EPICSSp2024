#The purpose of this file is to host the choose your chapter screen that follows the choose your
#eventually a difficulty setting will be integrated here or on the settings page?

#import necessary systems
import pygame
import os

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def chapter_select(screen,menuGraphics):

    window_width, window_height = screen.get_width(), screen.get_height()
    positionslist = [(int(window_width/6),int(7*window_height/12)),(int(window_width/2),int(7*window_height/12)),
        (int(5*window_width/6),int(7*window_height/12))]
    position = 0
 
    chap1_name = pygame.image.load(os.path.join('Assets',"scam1.png")) #change this .png file
    chap1_name = pygame.transform.scale(chap1_name,(int(window_width/3),int(window_height/3))) #dimensions here are to set how big you want it
    chap2_name = pygame.image.load(os.path.join('Assets',"scam2.png"))
    chap2_name=  pygame.transform.scale(chap2_name,(int(window_width/3),int(window_height/3)))#add chap1 and chap3
    chap3_name = pygame.image.load(os.path.join('Assets',"scam3.png"))
    chap3_name=  pygame.transform.scale(chap3_name,(int(window_width/3),int(window_height/3)))

    def draw_chapter_screen(screen,menuGraphics,window_width,window_height):
        screen.blit(menuGraphics['background'], (0,0))
        screen.blit(chap1_name, (int(3*window_width/120),int(3*window_height/60))) #dimensions here to set where on page you want it
        screen.blit(chap2_name, (int(3*window_width/9),int(3*window_height/60))) #dimensions here to set where on page you want it#chap2
        screen.blit(chap3_name, (int(3*window_width/4.7),int(3*window_height/60)))    #chap3
        
        screen.blit(menuGraphics['chap1'],(int(window_width/16),int(window_height/4)))
        screen.blit(menuGraphics['chap2'],(int(3*window_width/8),int(window_height/4)))
        screen.blit(menuGraphics['chap3'],(int(11*window_width/16),int(window_height/4)))
        screen.blit(menuGraphics['indicator'],positionslist[position])
        pygame.display.update()
    draw_chapter_screen(screen,menuGraphics,window_width,window_height)

    #JOYSTICK
    if joysticks:  #Checks if the joystick is connected. If not the arrow keys are used
        joystick = pygame.joystick.Joystick(0)
        #position = round(joystick.get_axis(0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and position < 2:
                    position += 1
                elif event.key == pygame.K_LEFT and position > 0:
                    position -= 1
                draw_chapter_screen(screen,menuGraphics,window_width,window_height)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return position
                
            #JOYSTICK
            elif joysticks: # For keys up and down, move
                if round(joystick.get_axis(0)) == -1 and position > 0: # Moving joystick left
                    position -= 1
                elif round(joystick.get_axis(0)) == 1 and position < 2: # Moving joystick right
                    position += 1
                draw_chapter_screen(screen,menuGraphics,window_width,window_height)
                if pygame.joystick.Joystick(0).get_button(0):
                    return position
