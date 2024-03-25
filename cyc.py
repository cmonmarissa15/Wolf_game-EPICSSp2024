#The purpose of this file is to host the choose your character screen that follows the main menu
#eventually a difficulty setting will be integrated here or on the settings page?

#import necessary systems
import pygame

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def character_select(screen,menuGraphics):
    window_width, window_height = screen.get_width(), screen.get_height()
    settingsfile = open("settings.txt",'r')
    currentsettings = settingsfile.readlines()
    settingsfile.close()
    indicator1rad, ypos1, ypos2 = int(window_height/24), int(window_height/2)-int(window_height)/24, window_height-int(window_height/24)
    positions1list = [(int(window_width/6)-indicator1rad,ypos1),(int(window_width/2)-indicator1rad,ypos1),(int(5*window_width/6)-indicator1rad,ypos1),
        (int(window_width/6)-indicator1rad,ypos2),(int(window_width/2)-indicator1rad,ypos2),(int(5*window_width/6)-indicator1rad,ypos2)]
    position1 = int(currentsettings[2][0]) # Current character is chosen by number on third line of settings file.

    color = (0,0,0)                        # text has color black
    smallfont = pygame.font.SysFont('constantia',60) # defining a font  
  
    # rendering text for each wolf for later use
    Aspen = smallfont.render('Aspen', True,color)
    Mani = smallfont.render('Máni', True , color)
    Kewa = smallfont.render('Khewa', True , color)
    Nico = smallfont.render('Niko', True , color)
    Sparrow = smallfont.render('Sparrow', True , color)
    Timber = smallfont.render('Timber', True , color)
    
    
    def draw_char_screen(screen,menuGraphics,window_width,window_height):
        
        
        screen.blit(menuGraphics['background'], (0,0)) # Portrait widths may vary, so justify.
        screen.blit(menuGraphics['topleftwolf'],(int(window_width/6-menuGraphics['topleftwolf'].get_width()/2),int(window_height/12)))
        screen.blit(menuGraphics['topcentwolf'],(int(window_width/2-menuGraphics['topcentwolf'].get_width()/2),int(window_height/12)))
        screen.blit(menuGraphics['topritewolf'],(int(5*window_width/6-menuGraphics['topritewolf'].get_width()/2),int(window_height/12)))
        screen.blit(menuGraphics['basleftwolf'],(int(window_width/6-menuGraphics['basleftwolf'].get_width()/2),int(7*window_height/12)))
        screen.blit(menuGraphics['bascentwolf'],(int(window_width/2-menuGraphics['bascentwolf'].get_width()/2),int(7*window_height/12)))
        screen.blit(menuGraphics['basritewolf'],(int(5*window_width/6-menuGraphics['basritewolf'].get_width()/2),int(7*window_height/12)))
        screen.blit(menuGraphics['indicator'],positions1list[position1])
        
        #Labelling for the wolves' names
        screen.blit(Aspen, (window_width/10, window_height/20))
        screen.blit(Kewa, (window_width/2.25, window_height/20))
        screen.blit(Mani, (window_width/1.3, window_height/20))
        screen.blit(Nico, (window_width/10, window_height/1.8))
        screen.blit(Sparrow, (window_width/2.25, window_height/1.8))
        screen.blit(Timber, (window_width/1.3, window_height/1.8))
        
        pygame.display.update()
        
    draw_char_screen(screen,menuGraphics,window_width,window_height)

    runningcyc = True

    #JOYSTICK
    if joysticks:  #Checks if the joystick is connected. If not the arrow keys are used
        joystick = pygame.joystick.Joystick(0)
        #position1 = round(joystick.get_axis(0))

    while runningcyc:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and position1 % 3 != 2:
                    position1 += 1
                elif event.key == pygame.K_LEFT and position1 % 3 != 0:
                    position1 -= 1
                elif event.key == pygame.K_UP and position1 > 2:
                    position1 -= 3
                elif event.key == pygame.K_DOWN and position1 < 3:
                    position1 += 3
                draw_char_screen(screen,menuGraphics,window_width,window_height)
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    currentsettings[2] = str(position1) + '\n'
                    settingsfile = open("settings.txt",'w')
                    for eachline in currentsettings:
                        settingsfile.write(eachline)
                    settingsfile.close()
                    runningcyc = False
                
            #JOYSTICK
            elif joysticks: 
                if round(joystick.get_axis(1)) == -1 and position1 > 2: # Moving joystick up
                    position1 -= 3
                elif round(joystick.get_axis(1)) == 1 and position1 < 3: # Moving joystick down
                    position1 += 3
                elif round(joystick.get_axis(0)) == 1 and position1 % 3 != 2: # Moving joystick right
                    position1 += 1  
                elif round(joystick.get_axis(0)) == -1 and position1 % 3 != 0: # Moving joystick left
                    position1 -= 1 
                draw_char_screen(screen,menuGraphics,window_width,window_height)
                if pygame.joystick.Joystick(0).get_button(0):
                    currentsettings[2] = str(position1) + '\n'
                    settingsfile = open("settings.txt",'w')
                    for eachline in currentsettings:
                        settingsfile.write(eachline)
                    settingsfile.close()
                    runningcyc = False
