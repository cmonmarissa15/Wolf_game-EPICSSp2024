# Chapter 2
# The search for a den somewhere in the world.

from worldgeneration import *
from gamethods import *
import random
import dialog
import pygame
import huntgame

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def run_second_chapter(screen, worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics):
    
    
    globinfo = readglobals()
    window_width = globinfo['window_width']
    window_height = globinfo['window_height']

    color = (0,0,0)                        # text has color black
    smallfont = pygame.font.SysFont('constantia',30) # defining a font  
  
    # rendering text for each species for later use
    player_food = smallfont.render('Health' , True , color)

    # Make a world for this chapter.
    
    # globinfo = readglobals()
    #     window_width = globinfo['window_width']
    #     window_height = globinfo['window_height']
    #     timelapsed = 0
    #     frame_time = globinfo['frame_time']
    #     pygame.time.delay(frame_time)
    
    chapterworld = generateWorld(worldx,worldy,window_width,window_height,background, nightbackground, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalGraphics)
    ybaselist = getYbaselist(chapterworld.objectsofheight)

    charname, framelists = getCharacterData(wolfGraphics)

    inchapter = True

    # Player will re-discover these things from chapter one.
    metworldedge = False
    methuman = False

    # Our objective
    foundnewpack = False

    playerx = random.randint(0,worldx)
    playery = random.randint(0,worldy)
    while not (posok(playerx,playery,chapterworld.obstacles) and posinworld(playerx,playery,worldx,worldy,window_width,window_height)):
        playerx = random.randint(0,worldx)
        playery = random.randint(0,worldy)

    currentmode = 0
    currentframe = 0

    health = 100 # Health carries over from file.
    timelapsed = 0
    night = False
    frame_time = globinfo['frame_time']
    
    # Define initial time and clock
    time_left = 500  # Initial time in seconds
    clock = pygame.time.Clock()

    drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe, player_food,time_left)
    dialog.akela(screen,"On behalf of the pack, I wish you well in your search for a new family.")
    dialog.akela(screen,"You'll be hunting alone for now, until you find your new den.")
    dialog.dialog(screen,"Akela",['Dens look like this and are usually found near water.'],miscellaneousGraphics['den'])

    while inchapter:
        time_left -= 1
        if time_left < 0:
            time_left = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
        pressed = pygame.key.get_pressed() # This method of movement checking
        newposx = playerx                  # considers all keys which may be
        newposy = playery                  # pressed at the end of a tick/frame.
        if pressed[pygame.K_RIGHT]:
            newposx += 1
        if pressed[pygame.K_LEFT]:
            newposx -= 1
        if pressed[pygame.K_UP]:
            newposy -= 1
        if pressed[pygame.K_DOWN]:
            newposy += 1
        if pressed[pygame.K_RETURN]:
            speed = 40
            health -= 0.1
        else:
            speed = 10

        #JOYSTICK
        if joysticks:  #Checks if the joystick is connected. If not the arrow keys are used
            joystick = pygame.joystick.Joystick(0)

            if pygame.joystick.Joystick(0).get_button(1):
                speed = 40
            else:
                speed = 10
                    
            joyx = round(joystick.get_axis(0))
            joyy = round(joystick.get_axis(1))

            newposx = playerx + int(joyx * speed)
            newposy = playery + int(joyy * speed) 

            pygame.display.update() 
            
        # Newpos variables currently indicate only the direction of motion as a
        # vector of variable magnitude.
        dist = ((newposx-playerx)**2 + (newposy-playery)**2) ** 0.5
        if dist > 0:
            newposx = playerx + (newposx - playerx)*speed/dist
            newposy = playery + (newposy - playery)*speed/dist
        # Newpos variables now indicate the desired position of the player in the
        # next frame.
            if newposx > playerx:   # When choosing the direction to face the
                currentmode = 0     # player, left and right are prioritized for
            elif newposx < playerx: # diagonals, as in the Champion Island game.
                currentmode = 1
            elif newposy > playery:
                currentmode = 2
            elif newposy < playery:
                currentmode = 3
        if posok(newposx,newposy,chapterworld.obstacles) and posinworld(newposx,newposy,worldx,worldy,window_width,window_height):
            playerx,playery = newposx,newposy # Player position changes;
        elif metworldedge == False and not posinworld(newposx,newposy,worldx,worldy,window_width,window_height):
            metworldedge = True
            dialog.selfnote(screen,"Doesn't smell like there are any wolves that way.",framelists[4])
        # Newpos variables now reflect current position.
        doesCol = intCol(newposx,newposy,chapterworld.interactives)
        if doesCol:
            if isinstance(doesCol,Print):
                animal = doesCol.animal
                guesses = [animal]
                guesses.extend(random.sample(list(printGraphics)+['bear','fox','wolf'],3))
                if guesses.count(animal) > 1:
                    guesses.remove(animal)
                random.shuffle(guesses)
                correctans = guesses.index(animal)
                specguess = dialog.dialog(screen,"What kind of tracks are these?",guesses,printGraphics[animal])
                if specguess == correctans:
                    # dialog.selfnote(screen,"That's right!",framelists[4])
                    # dialog.selfnote(screen,"That's right!")
                    dialog.akela(screen,"Very good!")
                else:
                    # dialog.selfnote(screen,"No, that's not right.",framelists[4])
                    # dialog.selfnote(screen,"No, that's not right.")
                    dialog.akela(screen,"Actually, those are "+animal+" tracks.")

                actions = ['Hunt','Ignore it','Run away']
                actguess = dialog.dialog(screen,"What to do?",actions,printGraphics[animal])
                if guesses == 'bison':
                    dialog.selfnote(screen,"RUN!!!",framelists[4])
                if actguess == 0:
                    # Connect the hunting mini-game here!!!!
                    writeHealth(health)
                    borders, huntworld = makeHuntWorld(chapterworld,playerx,playery,window_width,window_height,animal,animalGraphics,night,True,wolfGraphics,charname,5)
                    huntgame.run_hunting_game(screen,borders,huntworld,timelapsed,night,framelists,wolfGraphics,False)
                    health = readHealth()                                              # If pup, send later framelists.
                doesCol.xpos = -1000
                drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe,player_food,time_left)
            elif isinstance(doesCol,Settlement): # Code for other interactives - like the den - go here.
                if doesCol.human and not methuman:
                    dialog.selfnote(screen,"Smells like human. I'd better look out.",framelists[4])
                    methuman = True
                elif not doesCol.human:
                    foundnewpack = True

        if dist > 0: # If player moves, update animation frame in list.
            if currentframe != len(framelists[currentmode]) - 1:
                currentframe += 1
            else:
                currentframe = 2 # Reset to third frame to loop
        else:
            currentframe = 0 # If player doesn't move, return to standing.

        drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe,player_food,time_left)
        pygame.time.delay(frame_time)
        timelapsed += 1
        if timelapsed == 500: # Should be 2400 ticks per year.
            inchapter = False
        # elif timelapsed % 600 == 0:
        #     night = False
        # elif timelapsed % 300 == 0:
        #     night = True
        if health < 0:
            dialog.akela(screen,"You ran out of health while trying to find the den. Better luck next time!")
            return 1
        if foundnewpack:
            dialog.akela(screen,"I see you've found a new home!  I wish you well in your endeavors.")
            return dialog.dialog(screen,"What would you like to do now?",['Find my new pack!','Return to the main menu'])
    dialog.akela(screen,"Winter came, and you did not find a home.  It seems you will be a lone wolf forever.")
    return 1
