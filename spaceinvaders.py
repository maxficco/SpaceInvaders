import pygame
import random

pygame.init()
pygame.display.set_caption("Space Invaders Clone - by Max Ficco")
width = 1200
height = 800
screen = pygame.display.set_mode((width,height))

alien1a = pygame.transform.scale(pygame.image.load(f"alien1a.png").convert_alpha(), (44,32))
alien1b = pygame.transform.scale(pygame.image.load(f"alien1b.png").convert_alpha(), (44,32))
alien2a = pygame.transform.scale(pygame.image.load(f"alien2a.png").convert_alpha(), (44,32))
alien2b = pygame.transform.scale(pygame.image.load(f"alien2b.png").convert_alpha(), (44,32))
alien3a = pygame.transform.scale(pygame.image.load(f"alien3a.png").convert_alpha(), (44,32))
alien3b = pygame.transform.scale(pygame.image.load(f"alien3b.png").convert_alpha(), (44,32))

player = pygame.image.load("player.png").convert_alpha()
player = pygame.transform.scale(player, (60,52))
playerbox = pygame.Rect(width/2, 740,60,52)

gameRunning = True
dx = 20
px = 0
frameCount = 0
frameCountChange = 2
spritename = "a"
spaghetti = 0

playerBullets = []
enemyBullets = []

def setUpInvaders():
    aliensSetupList = []
    NUM_ROWS = 11
    NUM_INVADERS_PER_ROW = 5
    for row in range(NUM_ROWS):
        x = row*75
        for number in range(NUM_INVADERS_PER_ROW):
            y = number*75
            aliensSetupList.append(pygame.Rect(x,y,44,32))
    return aliensSetupList
alienList = setUpInvaders()

def drawInvaders(alienList, screen, spritename, spaghetti):
    for i in alienList:
        #pygame.draw.rect(screen, (255, 0, 0), i, 1)
        if spritename == "a":
            if (i.y - spaghetti*50)/75 == 0:
                screen.blit(alien3a, i)
            if ((i.y - spaghetti*50)/75 == 1) or ((i.y - spaghetti*50)/75 == 2):
                screen.blit(alien1a, i)
            if ((i.y - spaghetti*50)/75 == 3) or ((i.y - spaghetti*50)/75 == 4):
                screen.blit(alien2a, i)
        if spritename == "b":
            if (i.y - spaghetti*50)/75 == 0:
                screen.blit(alien3b, i)
            if ((i.y - spaghetti*50)/75 == 1) or ((i.y - spaghetti*50)/75 == 2):
                screen.blit(alien1b, i)
            if ((i.y - spaghetti*50)/75 == 3) or ((i.y - spaghetti*50)/75 == 4):
                screen.blit(alien2b, i)

def moveInvaders(alienList, dx, frameCountChange, spaghetti):
    for i in alienList:
        if i.right + dx > width or i.left + dx < 0:
            for alien in alienList:
                alien.y = alien.y+50
            dx = dx*-1
            spaghetti += 1
            frameCountChange = frameCountChange + 0.25
            break
    for i in alienList:
        i.x = i.x + dx
    return dx, frameCountChange, spaghetti

def changeSprites(spritename): 
    if spritename == "a":
        spritename = "b"
    elif spritename == "b":
        spritename = "a"
    return spritename

def makeBullet(playerbox, playerBullets, px):
    bullet = pygame.Rect(playerbox.x+30, playerbox.y, 2, 15)
    playerBullets.append(bullet)
    bulletxvel = px
    return playerBullets, bulletxvel

def makeBarriers():
    barriers = []
    NUM_ROWS = 9
    NUM_BLOCKS_PER_ROW = 3
    for row in range(NUM_ROWS):
        x = 100 + row*16
        for number in range(NUM_BLOCKS_PER_ROW):
            y = height - 100 - number*16
            barriers.append(pygame.Rect(x,y,16,16))
    for row in range(NUM_ROWS):
        x = width - 100 - row*16
        for number in range(NUM_BLOCKS_PER_ROW):
            y = height - 100 - number*16
            barriers.append(pygame.Rect(x,y,16,16))
    for row in range(NUM_ROWS):
        x = 300 + row*16
        for number in range(NUM_BLOCKS_PER_ROW):
            y = height - 100 - number*16
            barriers.append(pygame.Rect(x,y,16,16))
    for row in range(NUM_ROWS):
        x = width - 300 - row*16
        for number in range(NUM_BLOCKS_PER_ROW):
            y = height - 100 - number*16
            barriers.append(pygame.Rect(x,y,16,16))
    return barriers
barriers = makeBarriers()

def makeEnemyBullets(enemyBullets, alienList):
    shooter = random.choice(alienList)
    shooterBullet = pygame.Rect(shooter.x + 22, shooter.y, 4, 20)
    enemyBullets.append(shooterBullet)
    return enemyBullets

while gameRunning:
    # Reset Screen
    screen.fill((0,0,0))
    
    # Check for Pygame Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Reset Velocity of Player If At Edge
                if px > 0:
                    px = 0
            if event.key == pygame.K_RIGHT:
                # Reset Velocity of Player If At Edge
                if px < 0:
                    px = 0
            if event.key == pygame.K_SPACE:
                # Create Bullet and Add To List
                if len(playerBullets) < 1:
                    playerBullets, bulletxvel = makeBullet(playerbox, playerBullets, px)

    # Register Key Presses and Change Player Velocity
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and playerbox.left >=0:
        if px > -4:
            px = px -0.5 
    if keys_pressed[pygame.K_RIGHT] and playerbox.right <= width:
        if px < 4:
            px = px +0.5 
    else:
        # Slowly Decrease Player Velocity (Gliding Effect)
        if px >0:
            px = px -0.125
        else:
            px = px +0.125 


    # Internal Clock That Speeds Up
    if frameCount >= 100:
        # Move Invaders
        dx, frameCountChange, spaghetti = moveInvaders(alienList, dx, frameCountChange, spaghetti)
        # Change Sprite
        spritename = changeSprites(spritename)
        # Make Enemy Bullet
        if len(enemyBullets) < len(alienList)/11:
            enemyBullets = makeEnemyBullets(enemyBullets, alienList)
        frameCount = 0
    frameCount += frameCountChange

    # Move Player
    if playerbox.left + px < 0 or playerbox.right + px > width :
        px = 0
    else:
        playerbox.x = playerbox.x + px
    
    # Draw Bullets and Check Collisions
    for bullet in playerBullets:
        pygame.draw.rect(screen, (255,0,0), bullet)
        bullet.y = bullet.y - 10
        bullet.x = bullet.x + bulletxvel*0.75
        if bullet.y < 0:
            playerBullets.remove(bullet)
        for a in alienList:
            if bullet.colliderect(a):
                alienList.remove(a)
                playerBullets.remove(bullet)
    # Draw Invaders
    drawInvaders(alienList, screen, spritename, spaghetti)
    
    # Draw Player
    screen.blit(player, playerbox)
    #pygame.draw.rect(screen, (255, 0, 0), playerbox, 1)
    
    # Draw Barriers and Check Collisions
    for barrier in barriers:
        pygame.draw.rect(screen, (0,255,0), barrier)
        for b in playerBullets:
            if b.colliderect(barrier):
                playerBullets.remove(b)
                barriers.remove(barrier)
        for a in alienList:
            if a.colliderect(barrier):
                barriers.remove(barrier)
        for e in enemyBullets:
            if e.colliderect(barrier):
                enemyBullets.remove(e)
                barriers.remove(barrier)
    
    # Draw Enemy Bullets and Check Collisions
    for ebullet in enemyBullets:
        pygame.draw.rect(screen, (0,255,0), ebullet)
        ebullet.y = ebullet.y + 4 
        if ebullet.y > height:
            enemyBullets.remove(ebullet)
        if ebullet.colliderect(playerbox):
            enemyBullets.remove(ebullet)
            gameRunning = False
        for z in playerBullets:
            if z.colliderect(ebullet):
                enemyBullets.remove(ebullet)
                playerBullets.remove(z)

    pygame.display.update()
    pygame.time.delay(10)
