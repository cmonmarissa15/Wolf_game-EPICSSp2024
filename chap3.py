# Chapter 3
# Featuring a young wolf who is new to the world.

from worldgen_chap3 import *
from gamethods import *
import random
import dialog
import pygame
import huntgame
import huntgame_chap3

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def run_third_chapter(screen, worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics):
    globinfo = readglobals()
    window_width = globinfo['window_width']
    window_height = globinfo['window_height']

    color = (0,0,0)                        # text has color black
    smallfont = pygame.font.SysFont('constantia',30) # defining a font  
  
    # rendering text for each species for later use
    player_food = smallfont.render('Health' , True , color)

    # Make a world for this chapter.
    chapterworld = generateWorld_3(worldx,worldy,window_width,window_height,background, nightbackground, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalGraphics)
    ybaselist = getYbaselist(chapterworld.objectsofheight)

    charname, framelists = getCharacterData(wolfGraphics)

    inchapter = True
    metworldedge = False
    metprey = False
    metpredator = False
    metignore = False
    metperson = False

    playerx = random.randint(0,worldx)
    playery = random.randint(0,worldy)
    while not (posok(playerx,playery,chapterworld.obstacles) and posinworld(playerx,playery,worldx,worldy,window_width,window_height)):
        playerx = random.randint(0,worldx)
        playery = random.randint(0,worldy)

    currentmode = 0
    currentframe = 0
    
    health = 100
    writeHealth(health)
    timelapsed = 0
    night = False
    frame_time = globinfo['frame_time']
    hunt = 0
    
    # Define initial time and clock
    time_left = 500  # Initial time in seconds
    clock = pygame.time.Clock()

    drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe, player_food, time_left)
    dialog.akela(screen,"Congratulations on finding your den!")
    dialog.akela(screen,"Now that you've found your home, it's time to find your family")
    dialog.akela(screen,"You must keep your family fed for a year to keep your staus as pack leader")

    wolf_counter = 0
    while inchapter:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If 'x' button selected, end
                return 'stop'
            
        time_left -= 1
        if time_left < 0:
            time_left = 0 
            
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
            dialog.akela(screen,"The map background is only so big.")
        # Newpos variables now reflect current position.
        
        
        
        doesCol = intCol(newposx,newposy,chapterworld.interactives)
        if doesCol:
            if isinstance(doesCol,Print):
                animal = doesCol.animal
                
                if(animal == 'wolf'):
                    wolf_counter += 1
                    # wolf_number += 1
                    wolf_number  = str(wolf_counter)
                    dialog.akela(screen,"Looks like you found Wolf Print(s)" + wolf_number)
                    # doesCol.xpos = -1000
                    # drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe, player_food, time_left)
                    
                    if(wolf_counter == 5):
                        dialog.akela(screen,"Looks like you found all the Wolf Prints")
                        dialog.akela(screen,"Now it's time to hunt the biggest of them all.")
                        dialog.akela(screen,"Hunt a bison to win the game!")
                        
                        # refusehunt = dialog.dialog(screen,"Ready to hunt?",['Yes','No'],printGraphics[animal]) # Pick better image?
                        # if refusehunt:
                            # dialog.akela(screen,"Okay, but be sure to let me know if you find another bison track.")
                        # else: #accepting hunt
                        # dialog.akela(screen,"Then let's go hunt together!")
                            # if metpredator:
                            #     dialog.akela(screen,"Good luck!")
                            # elif not metprey: # other than bison
                        if(animal == 'bison'):
                            dialog.akela(screen,"I'll bring the rest of the pack to help you!")
                            metprey = True #this is a rabbit and deer
                            writeHealth(health)
                            borders, huntworld = makeHuntWorld(chapterworld,playerx,playery,window_width,window_height,animal,animalGraphics,night,True,wolfGraphics,charname,5)
                            huntgame_chap3.run_hunting_game_chap3(screen,borders,huntworld,timelapsed,night,framelists[5:],wolfGraphics,True) #only diffference is that with this huntgame, you can hurt the bison
                            health = readHealth() 
                            hunt += 1
                
                else:
                    dialog.akela(screen,"Looks like you've found some tracks!")
                    guesses = [animal]
                    guesses.extend(random.sample(list(printGraphics)+['bear','fox','raccoon','beaver','turtle','badger','coyote','puma','wolf'],3))
                    if guesses.count(animal) > 1:
                        guesses.remove(animal)
                    random.shuffle(guesses)
                    correctans = guesses.index(animal)
                    specguess = dialog.dialog(screen,"What kind of tracks are these?",guesses,printGraphics[animal])
                    if specguess == correctans:
                        dialog.akela(screen,"Very good!")
                    else:
                        dialog.akela(screen,"Actually, those are "+animal+" tracks.")
                    actions = ['Hunt','Ignore it','Run away']
                    actguess = dialog.dialog(screen,"What do you do when you see "+animal+" tracks?",actions,printGraphics[animal])

                    # if actguess == animalTypes[animal]:
                    if actguess == 2:
                        dialog.akela(screen,"That's right!")
                    elif actguess == 1:
                        metignore = True
                    elif isinstance(doesCol,Settlement): # Code for other interactives - like the den - go here.
                        if not methuman and doesCol.human:
                            dialog.akela(screen,"Be careful - humans live nearby.")
                            methuman = True
                    else:
                        dialog.akela(screen,"When you see "+animal+" tracks, you should "+actions[animalTypes[animal]]+".")
                        # dialog.selfnote(screen,"RUN!!!",framelists[4])


                    # if animalTypes[animal] == 0:
                    # if actguess != 0:
                        refusehunt = dialog.dialog(screen,"Ready to hunt?",['Yes','No'],printGraphics[animal]) # Pick better image?
                    
                        if refusehunt:
                            dialog.akela(screen,"Okay, but be sure to let me know if you find another track.")
                        else: #accepting hunt
                            dialog.akela(screen,"Then let's go hunt together!")
                            if metpredator:
                                dialog.akela(screen,"Good luck!")
                            elif not metprey: # other than bison
                                dialog.akela(screen,"I'll bring three other wolves from our pack to help you surround the animal.")
                            metprey = True #this is a rabbit and deer
                            writeHealth(health)
                            borders, huntworld = makeHuntWorld(chapterworld,playerx,playery,window_width,window_height,animal,animalGraphics,night,True,wolfGraphics,charname,5)
                            huntgame.run_hunting_game(screen,borders,huntworld,timelapsed,night,framelists[5:],wolfGraphics,True)
                            health = readHealth() 
                            hunt += 1
                            # Connect the hunting mini-game here!!!!


                    # else:
                    #     metpredator = True
                        
                doesCol.xpos = -1000
                drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe, player_food, time_left)
            elif isinstance(intCol,list): # Code for other interactives - like the den - go here.
                pass

        if dist > 0: # If player moves, update animation frame in list.
            if currentframe != len(framelists[currentmode]) - 1:
                currentframe += 1
            else:
                currentframe = 2 # Reset to third frame to loop
        else:
            currentframe = 0 # If player doesn't move, return to standing.

        drawScreen(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,currentmode,currentframe, player_food, time_left)
        pygame.time.delay(frame_time)
        timelapsed += 1
        if timelapsed == 500: # Should be 2400 ticks per year.  Set to 20 for testing.
            inchapter = False
            dialog.akela(screen,"Your pack left because they did not have enough food.")
            return 0
        # elif timelapsed % 600 == 0:
        #     night = False
        # elif timelapsed % 300 == 0:
        #     night = True
        if hunt >= 5:
            dialog.akela(screen,"Your pack is well fed!")
            return 1
