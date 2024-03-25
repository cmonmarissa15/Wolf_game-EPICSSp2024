# Chapter 1
# Featuring a young wolf who is new to the world.

from worldgeneration import *
from gamethods import *
import random
import dialog
import pygame
import huntgame

height = 900
width = 1200

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

def run_first_chapter(screen, worldx, worldy, background, nightbackground, wolfGraphics, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalTypes, animalGraphics, secondyear=False):
    globinfo = readglobals()
    window_width = globinfo['window_width']
    window_height = globinfo['window_height']
    
    color = (0,0,0)                        # text has color black
    smallfont = pygame.font.SysFont('constantia',30) # defining a font  
  
    # rendering text for each species for later use
    NPC_food = smallfont.render('NPC Food Bar' , True , color)
    player_food = smallfont.render('Your Food Bar' , True , color)

    # Make a world for this chapter.
    chapterworld = generateWorld(worldx,worldy,window_width,window_height,background, nightbackground, streamAppearancesByAim, streamNightAppearancesByAim, streamDimensionsByAim, streamCurveCoefficients, treeGraphics, treeNightGraphics, treeGreenness, rockGraphics, rockNightGraphics, decorGraphics, decorNightGraphics, decorDynamics, printGraphicsSmall, miscellaneousGraphics, miscellaneousNightGraphics, animalGraphics)
    ybaselist = getYbaselist(chapterworld.objectsofheight)

    charname, framelists = getCharacterData(wolfGraphics)

    inchapter = True
    running = True
    metworldedge = False
    metprey = False
    metpredator = False
    metignore = False
    methuman = False

    playerx = chapterworld.settlements[0].xpos
    playery = chapterworld.settlements[0].ybase
    while not (posok(playerx,playery,chapterworld.obstacles) and posinworld(playerx,playery,worldx,worldy,window_width,window_height)):
        playerx += 1

    currentmode = 5 # Use smaller images for pup.
    currentframe = 0

    health = 1
    writeHealth(health)
    
    NPC_health = 1
    writeNPCHealth(NPC_health)

    timelapsed = 0
    night = False
    frame_time = globinfo['frame_time']
    
    # Define initial time and clock
    time_left = 500  # Initial time in seconds
    clock = pygame.time.Clock()
    
    drawScreenChap1(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,NPC_health,currentmode,currentframe,NPC_food,player_food,time_left)
    dialog.akela(screen,f"Welcome to the world, {charname}!")
    dialog.akela(screen,f"I am Akela, leader of this pack.")
    dialog.akela(screen,f"To be a big strong wolf, you need to hunt more food than the other cubs in the pack!")
    dialog.akela(screen,f"The other cubs food bar is on the left of the screen.")
    dialog.akela(screen,f"Your food bar is on the right side of the screen.")
    dialog.akela(screen,f"Good luck on your adventures {charname}!")
    train = dialog.dialog(screen,"Will you be needing a demonstration of the game's controls?",['No, thank you.','Yes, please!'])
    if train:
        dialog.akela(screen,f"Sure thing, {charname}.")
        dialog.akela(screen,f"Use the arrow buttons to move around.")

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
                currentmode = 5     # player, left and right are prioritized for
            elif newposx < playerx: # diagonals, as in the Champion Island game.
                currentmode = 6
            elif newposy > playery:
                currentmode = 7
            elif newposy < playery:
                currentmode = 8    # To access the smaller 'pup' frames use 5-8, not 0-3.
        if posok(newposx,newposy,chapterworld.obstacles) and posinworld(newposx,newposy,worldx,worldy,window_width,window_height):
            playerx,playery = newposx,newposy # Player position changes;
        elif metworldedge == False and not posinworld(newposx,newposy,worldx,worldy,window_width,window_height):
            metworldedge = True
            dialog.akela(screen,"Be careful not to venture beyond the pack's territory.")
        # Newpos variables now reflect current position.
        doesCol = intCol(newposx,newposy,chapterworld.interactives)
        if doesCol:
            if isinstance(doesCol,Print):
                animal = doesCol.animal
                dialog.akela(screen,"Looks like you've found some tracks!")
                guesses = [animal]
                guesses.extend(random.sample(list(printGraphics)+['bear','fox','raccoon','beaver','turtle','badger','coyote','puma'],3))
                if guesses.count(animal) > 1:
                    guesses.remove(animal)
                random.shuffle(guesses)
                correctans = guesses.index(animal)
                specguess = dialog.dialog(screen,"What kind of tracks are these?",guesses,printGraphics[animal])
                if specguess == correctans:
                    dialog.akela(screen,"Very good!")
                else: 
                    dialog.akela(screen,"Actually, those are "+animal+" tracks.")
                actions = ['hunt','ignore it','run away']
                # actguess = dialog.akela(screen,"What do you do when you see "+animal+" tracks?",actions)
                actguess = dialog.dialog(screen,"What to do?",actions,printGraphics[animal])
                if guesses == 'bison':
                    dialog.selfnote(screen,"RUN!!!",framelists[4])
                if actguess == animalTypes[animal]:
                    dialog.akela(screen,"That's right!")
                else:
                    dialog.akela(screen,"When you see "+animal+" tracks, you should "+actions[animalTypes[animal]]+".")
                if animalTypes[animal] == 0:
                    refusehunt = dialog.akela(screen,"Ready to hunt?",['Yes','No']) # Pick better image?
                    if refusehunt:
                        dialog.akela(screen,"Okay, but be sure to let me know if you find another track.")
                    else:
                        dialog.akela(screen,"Then let's go hunt together!")
                        if not metprey:
                            dialog.akela(screen,"I'll bring three other wolves from our pack to help you surround the animal.")
                        metprey = True
                        writeHealth(health)
                        borders, huntworld = makeHuntWorld(chapterworld,playerx,playery,window_width,window_height,animal,animalGraphics,night,True,wolfGraphics,charname,3)
                        huntgame.run_hunting_game(screen,borders,huntworld,timelapsed,night,framelists[5:],wolfGraphics,True)
                        health = readHealth()                                              # If pup, send later framelists.
                elif animalTypes[animal] == 1:
                    metignore = True
                else:
                    metpredator = True
                doesCol.xpos = -1000
                drawScreenChap1(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,NPC_health,currentmode,currentframe, NPC_food, player_food,time_left)
            elif isinstance(doesCol,Settlement): # Code for other interactives - like the den - go here.
                if not methuman and doesCol.human:
                    dialog.akela(screen,"Be careful - humans live nearby.")
                    methuman = True

        if dist > 0: # If player moves, update animation frame in list.
            if currentframe != len(framelists[currentmode]) - 1:
                currentframe += 1
            else:
             currentframe = 2 # Reset to third frame to loop
        else:
            currentframe = 0 # If player doesn't move, return to standing.

        drawScreenChap1(screen,window_width,window_height,framelists,playerx,playery,chapterworld,ybaselist,timelapsed,night,health,NPC_health,currentmode,currentframe, NPC_food, player_food, time_left)
        pygame.time.delay(frame_time)
        timelapsed += 1
        if timelapsed == 500: # Should be 2400 ticks per year.
            inchapter = False
        NPC_health += .1
        if health >= 100: #2400 before # Should be 2400 ticks per year.  Set to 20 for testing.
            inchapter = False
        if NPC_health >= 100:
            inchapter = False
        # elif timelapsed % 600 == 0:
        #     night = False
        # elif timelapsed % 300 == 0:
        #     night = True
        # Training events here:
        if timelapsed == 20 and train:
            dialog.akela(screen,"Hold the select button/space bar/enter key to run.")
        elif timelapsed == 40 and train:
            dialog.akela(screen,"In the lower right is a gauge of your health.")
            dialog.akela(screen,"When you run, you tire a little and lose health.")
            dialog.akela(screen,"You can get energy again by eating - if you can catch food.")
            dialog.akela(screen,"Look around for tracks to start hunting.")
            train = True
    if health >= 100: #2400 before # Should be 2400 ticks per year.  Set to 20 for testing.
        inchapter = False
        dialog.akela(screen,"Congratualtaions! You beat the other wolf cub and are now ready to go out on your own.")
        if secondyear == False:
            return dialog.dialog(screen,"What would you like to do now?",['Stay with pack another year','Move on to next chapter','Return to the main menu'])
    if NPC_health >= 100:
        inchapter = False
        dialog.akela(screen,"Oh No! The wolf cub beat you! You may not be ready to go out on your own, but if you feel ready, we will let you.")
        if secondyear == False:
            return dialog.dialog(screen,"What would you like to do now?",['Restart chapter','Move on to next chapter','Return to the main menu'])