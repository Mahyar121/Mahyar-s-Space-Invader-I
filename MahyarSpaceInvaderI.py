'''
Mahyar Haji Babaie
mahyarhajibabaie@csu.fullerton.edu
game page
'''
import pygame
from pygame.locals import *
import random
import os
import json

pygame.init()

#class for the game Mahyar's Space Invader I
class MahyarSpaceInvaderI:
    def __init__(self):
        self.fileName = "HighScore.json"
        self.score = 0
        self.hard = False
        self.normal = False
        self.beginner = False
        self.userName = ""
        self.highScoreList = []
        self.lives = 3
        self.smallText = pygame.font.Font("game_font.ttf", 40)
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.teal = (0, 200, 255)
        self.green = (0, 200, 0)
        self.brightGreen = (0, 255, 0)
        self.pink = (240, 108, 227)
        self.red = (255, 0, 0)
        self.yellow = (255, 252, 124)
        self.black = (0, 0, 0)
        self.orange = (255, 125, 0)
        self.brightOrange = (255, 190, 0)
        self.lightPurple = (216, 191, 216)

        # if there is no file then make one
        if not os.path.isfile(self.fileName):
            empty_score_file = open(self.fileName, "w")
            empty_score_file.write("[]")
            empty_score_file.close()

        #setting up the font for the game
        pygame.font.init()
        self.font = pygame.font.Font("game_font.ttf", 25)
        pygame.display.set_caption("Mahyar's Space Invader I")
        #the 1 is the colored portion of the barrier
        barrierDesign = [[], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                         [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]]
        self.display_width = 800
        self.display_height = 600
        # sets the display resolution
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        # the enemy sprites
        self.enemySprites = {
            0:[pygame.image.load("e1_0.png").convert(), pygame.image.load("e1_1.png").convert()],
            1:[pygame.image.load("e2_0.png").convert(), pygame.image.load("e2_1.png").convert()],
            2:[pygame.image.load("e3_0.png").convert(), pygame.image.load("e3_1.png").convert()],
        }
        # the player sprite
        self.player = pygame.image.load("player.png").convert()
        # bomb sprites
        self.bomb1 = pygame.image.load("rocket.png").convert()
        self.bomb2 = pygame.image.load("rocket2.png").convert()
        self.bombCurrentImage = 1
        self.bombCount = 10
        self.bomb = None




        pygame.display.set_icon(self.player)
        self.animationOn = 0
        self.direction = 1
        self.enemySpeed = 10
        self.lastEnemyMove = 0
        self.playerPosX = 400
        self.playerPosY = 550
        self.bullet = None
        self.bullets = []
        self.enemyBullet = None
        self.enemyBullets = []
        self.enemies = []
        self.barrierParticles = []
        self.enemycount = 50


        self.chance = 990

        barrierX = 50
        barrierY = 400
        space = 100

        #creating a barrier
        for offset in range(1,5):
            for b in barrierDesign:
                for b in b:
                    if b!= 0:
                        self.barrierParticles.append(pygame.Rect(barrierX + space * offset, barrierY, 5,5))
                    barrierX += 5
                barrierX = 50 * offset
                barrierY += 3
            barrierY = 400

# PLAY AGAIN ----------------------------------------------------------------------------------------------------------

    def playAgain(self):

        self.score = 0
        self.lives = 3
        self.userName = ""
        # the 1 is the colored portion of the barrier
        barrierDesign = [[], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                         [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                         [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]]
        # the enemy sprites
        self.enemySprites = {
            0: [pygame.image.load("e1_0.png").convert(), pygame.image.load("e1_1.png").convert()],
            1: [pygame.image.load("e2_0.png").convert(), pygame.image.load("e2_1.png").convert()],
            2: [pygame.image.load("e3_0.png").convert(), pygame.image.load("e3_1.png").convert()],
        }
        # the player sprite
        self.player = pygame.image.load("player.png").convert()
        # bomb sprites
        self.bomb1 = pygame.image.load("rocket.png").convert()
        self.bomb2 = pygame.image.load("rocket2.png").convert()
        self.bombCurrentImage = 1
        self.bombCount = 10
        self.bomb = None



        pygame.display.set_icon(self.player)
        self.animationOn = 0
        self.direction = 1
        self.enemySpeed = 10
        self.lastEnemyMove = 0
        self.playerPosX = 400
        self.playerPosY = 550
        self.bullet = None
        self.bullets = []
        self.enemyBullet = None
        self.enemyBullets = []
        self.enemies = []
        self.barrierParticles = []
        self.enemycount = 50


        self.chance = 990

        barrierX = 50
        barrierY = 400
        space = 100

        # creating a barrier
        for offset in range(1, 5):
            for b in barrierDesign:
                for b in b:
                    if b != 0:
                        self.barrierParticles.append(pygame.Rect(barrierX + space * offset, barrierY, 5, 5))
                    barrierX += 5
                barrierX = 50 * offset
                barrierY += 3
            barrierY = 400

        if self.beginner:
            self.bombCount = 30
            self.lives = 10
            self.chance = 997

        if self.hard:
            self.bombCount = 1
            self.lives = 1
            self.chance = 935

        if self.normal:
            self.bombCount = 10
            self.lives = 3
            self.chance = 990



# Player --------------------------------------------------------------------------------------------------------------
    #handles the buttons for the player
    def playerUpdate(self):
        key = pygame.key.get_pressed()
        if key[K_LEFT] or key[K_a] and self.playerPosX > 0:
            self.playerPosX -= 5
        if (key[K_RIGHT] or key[K_d]) and self.playerPosX < (self.display_width + 60) - self.player.get_width():
            self.playerPosX += 5
        if (key[K_UP] or key[K_w]) and self.playerPosY > 0:
            self.playerPosY -= 5
        if (key[K_DOWN] or key[K_s]) and self.playerPosY < (self.display_height + 60) - self.player.get_height():
            self.playerPosY += 5
        if key[K_SPACE] and not self.bullet:
            self.bullet = pygame.Rect(self.playerPosX + self.player.get_width() / 4, self.playerPosY - 15, 5, 10)
        if key[K_b] and not self.bomb and self.bombCount > 0:
            self.bomb = self.screen.blit(self.bomb1, (self.playerPosX + self.player.get_width() / 4, self.playerPosY - 15))

    def bulletUpdate(self):
        for i, enemy in enumerate(self.enemies):
            for j, enemy in enumerate(enemy):
                enemy = enemy[1]
                # if a bullet hits an enemy you get 100 points
                if self.bullet and enemy.colliderect(self.bullet):
                    self.enemies[i].pop(j)
                    self.enemycount -= 1
                    self.bullet = None
                    self.bomb = None
                    self.chance -= 1
                    if self.beginner:
                        self.score += 10
                    if self.hard:
                        self.score += 300
                    if self.normal:
                        self.score += 100

        for x in self.bullets:
        # speed of bullet
            x.y += 10
        # if bullets off the screen then remove it
            if x.y > 600:
                self.bullets.remove(x)
        if self.bullet:
            self.bullet.y -= 7
            if self.bullet.y < 0:
                self.bullet = None

        for b in self.barrierParticles:
            check = b.collidelist(self.bullets)
            if check != -1:
                self.barrierParticles.remove(b)
                self.bullets.pop(check)
            elif self.bullet and b.colliderect(self.bullet):
                self.barrierParticles.remove(b)
                self.bullet = None
                self.score -= 100
    def bombUpdate(self):
        for i, enemy in enumerate(self.enemies):
            for j, enemy in enumerate(enemy):
                enemy = enemy[1]
                # if a bomb hits an enemy you get 100 points
                if self.bomb and enemy.colliderect(self.bomb):
                    self.enemies[i].pop(j)
                    self.enemycount -= 1
                    self.bomb = None
                    self.chance -= 1
                    self.bombCount -= 1

        if self.bomb:
            # speed of bullet
            self.bomb.y -= 15
            # if bullets off the screen then remove it
            if self.bomb.y < 0:
                self.bomb = None
        for b in self.barrierParticles:
            if self.bomb and b.colliderect(self.bomb):
                self.barrierParticles.remove(b)
                self.bomb = None
                self.bombCount -= 1
                self.score -= 100


    def bombAnimation(self):
        if self.bombCurrentImage == 1:
            self.screen.blit(self.bomb1, (self.bomb.x,self.bomb.y))
        if self.bombCurrentImage == 2:
            self.screen.blit(self.bomb2, (self.bomb.x,self.bomb.y))
        if self.bombCurrentImage == 2:
            self.bombCurrentImage = 1
        else:
            self.bombCurrentImage += 1

    def resetPlayer(self):
        self.playerPosX = 400
        self.playerPosY = 550

# ENEMY ---------------------------------------------------------------------------------------------------------------
    def enemyCreate(self):
        startY = 50
        startX = 50

        # positioning the enemy sprites in the rows
        for rows in range(5):
            out = []
            if rows < 1:
                enemy = 2
            elif rows < 3:
                enemy = 1
            else:
                enemy = 0
            for columns in range(10):
                out.append((enemy, pygame.Rect(startX * columns, startY * rows, 35 , 35)))
            self.enemies.append(out)

    def enemyUpdate(self):
        if not self.lastEnemyMove:
            for enemy in self.enemies:
                for enemy in enemy:
                    enemy = enemy[1]
                    # if enemy collides with player then the player loses a life and resets position of player
                    if enemy.colliderect(pygame.Rect(self.playerPosX, self.playerPosY, self.player.get_width(),
                                                     self.player.get_height())):
                        self.lives -= 1
                        self.resetPlayer()
                    # the x position of the enemy
                    enemy.x += self.enemySpeed * self.direction
                    self.lastEnemyMove = 25
                    # if the enemy is in the map, move them down
                    if enemy.x >= 750 or enemy.x <= 0:
                        self.moveEnemiesDown()
                        self.direction *= -1

                    chance = random.randint(0, 1000)
                    # how often the enemy shoots
                    if chance > self.chance:
                        self.enemyBullets.append(pygame.Rect(enemy.x, enemy.y, 5, 10))
            if self.animationOn:
                self.animationOn -= 1
            else:
                self.animationOn += 1
        else:
            self.lastEnemyMove -= 1
            # moves enemy units down

    def moveEnemiesDown(self):
        for enemy in self.enemies:
            for enemy in enemy:
                enemy = enemy[1]
                enemy.y += 20

    def enemyBulletUpdate(self):
        if self.enemyBullet:
            self.enemyBullet.y -= 7
            if self.enemeyBullet.y < 0:
                self.enemyBullet = None
        for x in self.enemyBullets:
            #speed of bullet
            x.y += 7
            #if bullets off the screen then remove it
            if x.y > 600:
                self.enemyBullets.remove(x)
            # if bullets hits the player then remove a life and reset him
            if x.colliderect(pygame.Rect(self.playerPosX, self.playerPosY, self.player.get_width(), self.player.get_height())):
                self.lives -= 1
                self.enemyBullets.remove(x)
                self.resetPlayer()
        for b in self.barrierParticles:
            check = b.collidelist(self.enemyBullets)
            if check != -1:
                self.barrierParticles.remove(b)
                self.enemyBullets.pop(check)
            elif self.enemyBullet and b.colliderect(self.enemyBullet):
                self.barrierParticles.remove(b)
                self.enemyBullet = None



# Text and Buttons -----------------------------------------------------------------------------------------------------
    def text_objects(self, text, font):
        #white font
        textSurface = font.render(text, True, self.white)
        return textSurface, textSurface.get_rect()

    def buttonBorder(self, color, x, y, w, h):
        pygame.draw.rect(self.screen, color, (x, y, w, h))

    def textButton(self, txt, x, y, w, h, ):
        textSurface, textRectangle = self.text_objects(txt, self.smallText)
        textRectangle.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(textSurface, textRectangle)

# MainMenu -------------------------------------------------------------------------------------------------------------
    def gameIntroButton(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #Quit button
        if 275 + 260 > mouse[0] > 275 and 505 + 50 > mouse[1] > 505:
            self.buttonBorder(self.white, 270,500,270,60)
            self.buttonBorder(self.brightGreen,275,505,260,50)
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            self.buttonBorder(self.white,270,500,270,60)
            self.buttonBorder(self.green,275,505,260,50)
        self.textButton("Quit",275,505,260,50)
        # HighScores button
        if 275 + 260 > mouse[0] > 275 and 405 + 50 > mouse[1] > 405:
            self.buttonBorder(self.white, 270, 400, 270, 60)
            self.buttonBorder(self.brightGreen, 275, 405, 260, 50)
            if click[0] == 1:
                self.highScoresPage()
        else:
            self.buttonBorder(self.white, 270, 400, 270, 60)
            self.buttonBorder(self.green, 275, 405, 260, 50)
        self.textButton("High Scores", 275, 405, 260, 50)
        #Controls button
        if 275 + 260 > mouse[0] > 275 and 305 + 50 > mouse[1] > 305:
            self.buttonBorder(self.white, 270, 300, 270, 60)
            self.buttonBorder(self.brightGreen, 275, 305, 260, 50)
            if click[0] == 1:
                self.controlsPage()
        else:
            self.buttonBorder(self.white, 270, 300, 270, 60)
            self.buttonBorder(self.green,275,305,260,50)
        self.textButton("Controls",275,305,260,50)
        #Tutorial button
        if 275 + 260 > mouse[0] > 275 and 205 + 50 > mouse[1] > 205:
            self.buttonBorder(self.white, 270, 200, 270, 60)
            self.buttonBorder(self.brightGreen, 275, 205, 260, 50)
            if click[0] == 1:
                self.tutorialPage()
        else:
            self.buttonBorder(self.white, 270, 200, 270, 60)
            self.buttonBorder(self.green, 275, 205, 260, 50)
        self.textButton("Tutorial", 275, 205, 260, 50)
        #Play button
        if 275 + 260 > mouse[0] > 275 and 105 + 50 > mouse[1] > 105:
            self.buttonBorder(self.white,270,100,270,60)
            self.buttonBorder(self.brightGreen, 275,105,260,50)
            if click[0] == 1:
                self.gameDifficulty()
                self.run()
        else:
            self.buttonBorder(self.white, 270, 100, 270, 60)
            self.buttonBorder(self.green, 275, 105, 260, 50)
        self.textButton("Play",275,105,260,50)

    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #black screen
            self.screen.fill(self.black)
            bigText = pygame.font.Font("game_font.ttf", 60)
            textSurface, textRectange = self.text_objects("Mahyar's Space Invader I", bigText)
            textRectange.center = ((self.display_width/2), (self.display_height/15))
            self.screen.blit(textSurface, textRectange)
            #shows the buttons on the game menu screen
            self.gameIntroButton()
            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(15)
# Controls Page -------------------------------------------------------------------------------------------------------
    def controlButtons(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #quit button
        if 480 + 260 > mouse[0] > 480 and 545 + 40 > mouse[1] > 545:
            self.buttonBorder(self.white,475,540,290,50)
            self.buttonBorder(self.brightGreen,480,545,280,40)
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            self.buttonBorder(self.white, 475, 540, 290, 50)
            self.buttonBorder(self.green, 480, 545, 280, 40)
        self.textButton("Quit",480,545,280,40)
        #back button
        if 80 + 260 > mouse[0] > 80 and 545 + 40 > mouse[1] > 545:
            self.buttonBorder(self.white, 75, 540, 290, 50)
            self.buttonBorder(self.brightGreen, 80, 545, 280, 40)
            if click[0] == 1:
                self.game_intro()
        else:
            self.buttonBorder(self.white, 75, 540, 290, 50)
            self.buttonBorder(self.green, 80, 545, 280, 40)
        self.textButton("Back",80,545,280,40)
        # Control BUTTONS
        # Move Left
        self.buttonBorder(self.red,75,125,290,50)
        self.buttonBorder(self.teal,80,130,280,40)
        self.textButton("Move Left:",80,130,280,40)
        # left arrow
        self.buttonBorder(self.red, 475, 125, 290, 50)
        self.buttonBorder(self.teal, 480, 130, 280, 40)
        self.textButton("Left Arrow or A", 480, 130, 280, 40)
        # Move Right
        self.buttonBorder(self.red, 75, 195, 290, 50)
        self.buttonBorder(self.teal, 80, 200, 280, 40)
        self.textButton("Move Right:", 80, 200, 280, 40)
        # right arrow
        self.buttonBorder(self.red, 475, 195, 290, 50)
        self.buttonBorder(self.teal, 480, 200, 280, 40)
        self.textButton("Right Arrow or D", 480, 200, 280, 40)
        # Move Up
        self.buttonBorder(self.red, 75, 265, 290, 50)
        self.buttonBorder(self.teal, 80, 270, 280, 40)
        self.textButton("Move Up:", 80, 270, 280, 40)
        # up arrow
        self.buttonBorder(self.red, 475, 265, 290, 50)
        self.buttonBorder(self.teal, 480, 270, 280, 40)
        self.textButton("Up Arrow or W", 480, 270, 280, 40)
        # Move Down
        self.buttonBorder(self.red, 75, 335, 290, 50)
        self.buttonBorder(self.teal, 80, 340, 280, 40)
        self.textButton("Move Down:", 80, 340, 280, 40)
        # down arrow
        self.buttonBorder(self.red, 475, 335, 290, 50)
        self.buttonBorder(self.teal, 480, 340, 280, 40)
        self.textButton("Down Arrow or S", 480, 340, 280, 40)
        # Shoot
        self.buttonBorder(self.red, 75, 405, 290, 50)
        self.buttonBorder(self.teal, 80, 410, 280, 40)
        self.textButton("Shoot:", 80, 410, 280, 40)
        # Space Bar
        self.buttonBorder(self.red, 475, 405, 290, 50)
        self.buttonBorder(self.teal, 480, 410, 280, 40)
        self.textButton("SpaceBar", 480, 410, 280, 40)
        # Bomb
        self.buttonBorder(self.red, 75, 475, 290, 50)
        self.buttonBorder(self.teal, 80, 480, 280, 40)
        self.textButton("Bomb:", 80, 480, 280, 40)
        # B
        self.buttonBorder(self.red, 475, 475, 290, 50)
        self.buttonBorder(self.teal, 480, 480, 280, 40)
        self.textButton("B", 480, 480, 280, 40)

    def controlsPage(self):
        controls = True
        while controls:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # black screen
            self.screen.fill(self.black)
            bigText = pygame.font.Font("game_font.ttf", 60)
            textSurface, textRectange = self.text_objects("Mahyar's Space Invader I", bigText)
            textRectange.center = ((self.display_width / 2), (self.display_height / 15))
            self.screen.blit(textSurface, textRectange)


            textSurface, textRectangle = self.text_objects("Controls Page", self.smallText)
            textRectangle.center = ((self.display_width/2), (self.display_height / 6))
            self.screen.blit(textSurface, textRectangle)

            self.controlButtons()
            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(15)

# HighScores ----------------------------------------------------------------------------------------------------------
    def highScoresPage(self):
        padding_y = 0
        maxScores = 8  # We *could* paint every score, but it's not any good if you can't see them (because we run out of the screen).
        scoresCount = 1
        highScore = True
        self.screen.fill(self.black)
        with open(self.fileName) as highscore_file:
           self.highScoreList = json.load(highscore_file)
        while highScore:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            for score in self.highScoreList:
                if scoresCount <= maxScores and scoresCount <= len(self.highScoreList):
                    self.screen.blit(
                        pygame.font.Font("game_font.ttf", 50).render(str(scoresCount) + ".  " + str(score["name"]) + ": " + str(score["score"]), 1,
                                         self.white), (250, 140 + padding_y))
                    padding_y += 50
                    scoresCount += 1

            bigText = pygame.font.Font("game_font.ttf", 60)
            textSurface, textRectange = self.text_objects("Mahyar's Space Invader I", bigText)
            textRectange.center = ((self.display_width / 2), (self.display_height / 15))
            self.screen.blit(textSurface, textRectange)

            line = "_____________________________________________________________________"
            self.screen.blit(pygame.font.Font("game_font.ttf", 50).render(line, -1, self.green), (0, 80))
            self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("High Scores", -1, self.brightGreen), (270, 70))

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            # quit button
            if 505 + 280 > mouse[0] > 505 and 545 + 40 > mouse[1] > 545:
                self.buttonBorder(self.white, 500, 540, 290, 50)
                self.buttonBorder(self.brightGreen, 505, 545, 280, 40)
                if click[0] == 1:
                    pygame.quit()
                    quit()
            else:
                self.buttonBorder(self.white, 500, 540, 290, 50)
                self.buttonBorder(self.green, 505, 545, 280, 40)
            self.textButton("Quit", 505, 545, 280, 40)
            # back button
            if 25 + 280 > mouse[0] > 25 and 545 + 40 > mouse[1] > 545:
                self.buttonBorder(self.white, 20, 540, 290, 50)
                self.buttonBorder(self.brightGreen, 25, 545, 280, 40)
                if click[0] == 1:
                    self.game_intro()
            else:
                self.buttonBorder(self.white, 20, 540, 290, 50)
                self.buttonBorder(self.green, 25, 545, 280, 40)
            self.textButton("Back", 25, 545, 280, 40)
            pygame.display.update()



    def addHighScores(self):
        with open(self.fileName) as highscore_file:
            self.highScoreList = json.load(highscore_file)

        if not self.highScoreList == None: # Make sure the prev. scores are loaded.
            new_json_score = { # Create a JSON-object with the score, name
                    "name":self.userName,
                    "score":self.score,
                    }
            self.highScoreList.append(new_json_score) # Add the score to the list of scores.

            self.highScoreList = self.sortHighScores(self.highScoreList) # Sort the scores.

            highscore_file = open(self.fileName, "w")
            highscore_file.write(json.dumps(self.highScoreList)) # Save the list of scores to highscore.json


    def sortHighScores(self, json):
        scores_dict = dict()  # Create a dictionary object.
        sorted_list = list()  # Create a list object.

        for obj in json:
            scores_dict[
                # Add every score to a dictionary with its score as key.
                obj["score"]] = obj

        for key in sorted(scores_dict.keys(),
                          reverse=True):  # Read the sorted dictionary in reverse order (highest score first)...
            sorted_list.append(scores_dict[key])  # ...and add it to a list.

        return sorted_list  # Tada! Returns a sorted list.



    def getUserName(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.unicode.isalpha():
                        self.userName += event.unicode
                    elif event.key == K_BACKSPACE:
                        self.userName = self.userName[:-1]
                    elif event.key == K_RETURN:
                        self.addHighScores()
                        loop = False
                elif event.type == QUIT:
                    pygame.quit()
                    quit()
            self.screen.blit(pygame.font.Font("game_font.ttf", 50).render(self.userName, -1, self.white), (100, 500))
            pygame.display.update()
# Tutorial Page -------------------------------------------------------------------------------------------------------
    def tutorialPage(self):
        bombTimer = 20
        fpsCount = 0
        seconds = 5
        mainmenuSeconds = 0
        key = pygame.key.get_pressed()
        clock = pygame.time.Clock()
        tutorialCount = 0
        tutorialFPScount = 0
        FPS = 60
        left = False
        right = False
        up = False
        down = False
        fire = False
        bomb = False
        tutorialExit = False
        bigFont = pygame.font.Font("game_font.ttf", 40)
        medFont = pygame.font.Font("game_font.ttf", 30)
        while not tutorialExit:
            clock.tick(FPS)
            self.screen.fill(self.black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            for b in self.barrierParticles:
                pygame.draw.rect(self.screen, (100, 255, 100), b)
            self.screen.blit(pygame.font.Font("game_font.ttf", 23).render("Type q to exit tutorial", -1, self.brightGreen),(222, 10))
            self.screen.blit(self.player, (self.playerPosX, self.playerPosY))
            key = pygame.key.get_pressed()
            if key[K_LEFT] or key[K_a] and self.playerPosX > 0:
                self.playerPosX -= 5
                left = True
            if (key[K_RIGHT] or key[K_d]) and self.playerPosX < self.display_width - self.player.get_width() and left :
                self.playerPosX += 5
                right = True
            if (key[K_UP] or key[K_w]) and left and right and self.playerPosY > 0:
                self.playerPosY -= 5
                up = True
            if (key[K_DOWN] or key[K_s]) and left and right and up and self.playerPosY < self.display_height - self.player.get_height():
                self.playerPosY += 5
                down = True
            if key[K_SPACE]  and left and right and up and down and not self.bullet:
                fire = True
                self.bullet = pygame.Rect(self.playerPosX + self.player.get_width() / 4, self.playerPosY - 15, 5, 10)
            if key[K_b] and left and right and up and down and fire and not self.bomb and self.bombCount > 0:
                bomb = True
                self.bomb = self.screen.blit(self.bomb1,(self.playerPosX + self.player.get_width() / 4, self.playerPosY - 15))
            if key[K_q]:
                self.playAgain()
                self.game_intro()

            if not left:
                self.screen.blit(bigFont.render("Press A or Left Arrow to move left", -1, self.red), (10, 40))
            if left and not right and not up and not down and not fire and not bomb:
                self.screen.blit(bigFont.render("Press D or Right Arrow to move right", -1, self.teal), (10, 40))
            if left and right and not up and not down and not fire and not bomb:
                self.screen.blit(bigFont.render("Press W or Up Arrow to move up", -1, self.brightGreen), (10, 40))
            if left and right and up and not down and not fire and not bomb:
                self.screen.blit(bigFont.render("Press S or Down Arrow to move down", -1, self.yellow), (10, 40))
            if left and right and up and down and not fire and not bomb:
                self.screen.blit(bigFont.render("Press Spacebar to fire", -1, self.orange), (10, 40))
            if left and right and up and down and fire and not bomb:
                self.screen.blit(bigFont.render("Press B to release a bomb", -1, self.lightPurple), (10, 40))
            if left and right and up and down and fire and bomb and tutorialCount == 0:
                self.screen.blit(medFont.render("Remember you have a limited amount of bombs", -1, self.brightGreen), (0, 40))
                self.screen.blit(medFont.render("If the bomb timer equals 0 you get a new bomb", -1, self.red),(5, 80))
                self.screen.blit(medFont.render("Bombs give 0 points if it kills a target", -1, self.brightGreen),(15, 120))
                tutorialFPScount += 1
                if tutorialFPScount == 700:
                    tutorialCount += 1
            if tutorialCount == 1:
                self.screen.blit(medFont.render("You lose 100 points if you shoot at the barrier", -1, self.teal), (10, 40))
                self.screen.blit(medFont.render("Game Difficulty determines how many points per kill", -1, self.brightOrange),(10, 80))
                self.screen.blit(medFont.render("Use your bombs for emergency situations", -1, self.orange), (10, 120))
                tutorialFPScount += 1
                if tutorialFPScount == 1400:
                    tutorialCount += 1
            if tutorialCount == 2:
                self.screen.blit(bigFont.render("You will lose if your lives goes down to 0", -1, self.yellow),(10, 40))
                self.screen.blit(bigFont.render("You will win if you kill all the enemies", -1, self.red), (10, 80))
                tutorialFPScount += 1
                if tutorialFPScount == 1900:
                    tutorialCount += 1
            if tutorialCount == 3:
                self.screen.blit(bigFont.render("You have completed the Tutorial!", -1, self.teal),(10, 40))
                self.screen.blit(bigFont.render("Returning to MainMenu in {}".format(seconds), -1, self.lightPurple), (10, 80))
                mainmenuSeconds += 1
                if mainmenuSeconds == 70:
                    mainmenuSeconds = 0
                    seconds -= 1
                if seconds == 0:
                    self.playAgain()
                    self.game_intro()

            if bombTimer == 0:
                bombTimer = 20
                self.bombCount += 1
            if fpsCount == 60:
                fpsCount = 0
                bombTimer -= 1
            fpsCount += 1
            if self.bullet:
                pygame.draw.rect(self.screen, (52,255,0), self.bullet)
            if self.bomb:
                self.bombAnimation()
            self.bombUpdate()
            self.bulletUpdate()
            self.screen.blit(self.font.render("Lives: {}".format(self.lives), -1, self.white), (0, 10))
            self.screen.blit(self.font.render("Score: {}".format(self.score), -1, self.white), (450, 10))
            self.screen.blit(self.font.render("Bombs: {}".format(self.bombCount), -1, self.white), (100, 10))
            self.screen.blit(self.font.render("Bomb Timer: {}".format(bombTimer), -1, self.white), (620, 10))
            pygame.display.update()
# Game Difficulty ------------------------------------------------------------------------------------------------------

    def gameDifficulty(self):
        choosing = True
        clock = pygame.time.Clock()
        bigFont = pygame.font.Font("game_font.ttf", 60)
        medFont = pygame.font.Font("game_font.ttf", 40)
        smallFont = pygame.font.Font("game_font.ttf", 25)
        while choosing:
            # THE FPS
            clock.tick(60)
            # MAKES THE BACKGROUND BLACK
            self.screen.fill(self.black)
            # If someone clicks the X on the top right corner, exit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            # quit button
            if 495 + 280 > mouse[0] > 495 and 545 + 40 > mouse[1] > 545:
                self.buttonBorder(self.white, 490, 540, 290, 50)
                self.buttonBorder(self.brightGreen, 495, 545, 280, 40)
                if click[0] == 1:
                    pygame.quit()
                    quit()
            else:
                self.buttonBorder(self.white, 490, 540, 290, 50)
                self.buttonBorder(self.green, 495, 545, 280, 40)
            self.textButton("Quit", 495, 545, 280, 40)

            # back button
            if 25 + 260 > mouse[0] > 25 and 545 + 40 > mouse[1] > 545:
                self.buttonBorder(self.white, 20, 540, 290, 50)
                self.buttonBorder(self.brightGreen, 25, 545, 280, 40)
                if click[0] == 1:
                    self.game_intro()
            else:
                self.buttonBorder(self.white, 20, 540, 290, 50)
                self.buttonBorder(self.green, 25, 545, 280, 40)
            self.textButton("Back", 25, 545, 280, 40)

            # Beginner button
            if 25 + 260 > mouse[0] > 25 and 125 + 40 > mouse[1] > 125:
                self.buttonBorder(self.yellow, 20, 120, 290, 50)
                self.buttonBorder(self.pink, 25, 125, 280, 40)
                if click[0] == 1:
                    self.beginner = True
                    self.normal = False
                    self.hard = False
                    self.bombCount = 30
                    self.lives = 10
                    self.chance = 997
                    self.run()
            else:
                self.buttonBorder(self.yellow, 20, 120, 290, 50)
                self.buttonBorder(self.red, 25, 125, 280, 40)
            self.textButton("Beginner", 25, 125, 280, 40)

            # Normal button
            if 25 + 260 > mouse[0] > 25 and 265 + 40 > mouse[1] > 275:
                self.buttonBorder(self.yellow, 20, 260, 290, 50)
                self.buttonBorder(self.teal, 25, 265, 280, 40)
                if click[0] == 1:
                    self.normal = True
                    self.hard = False
                    self.beginner = False
                    self.bombCount = 10
                    self.lives = 3
                    self.chance = 990
                    self.run()
            else:
                self.buttonBorder(self.yellow, 20, 260, 290, 50)
                self.buttonBorder(self.blue, 25, 265, 280, 40)
            self.textButton("Normal", 25, 265, 280, 40)

            # Expert button
            if 25 + 260 > mouse[0] > 25 and 405 + 40 > mouse[1] > 405:
                self.buttonBorder(self.yellow, 20, 400, 290, 50)
                self.buttonBorder(self.brightOrange, 25, 405, 280, 40)
                if click[0] == 1:
                    self.hard = True
                    self.normal = False
                    self.beginner = False
                    self.bombCount = 1
                    self.lives = 1
                    self.chance = 935
                    self.run()
            else:
                self.buttonBorder(self.yellow, 20, 400, 290, 50)
                self.buttonBorder(self.orange, 25, 405, 280, 40)
            self.textButton("Expert", 25, 405, 280, 40)

            self.screen.blit(bigFont.render("Mahyar's Space Invader I", -1, self.white), (100, 0))
            self.screen.blit(medFont.render("Choose Your Game Difficulty", -1, self.teal), (170, 60))

            # beginner button description
            self.screen.blit(smallFont.render("Beginner Mode starts with 10 Lives, 30 Bombs, and less points per kill.", -1, self.yellow), (15, 185))
            self.screen.blit(smallFont.render("Beginner Mode makes the enemies shoot at a slow rate.", -1, self.yellow), (15, 215))

            # normal button description
            self.screen.blit(smallFont.render("Normal Mode starts with 3 Lives, 10 Bombs, and standard points per kill.", -1, self.yellow), (15, 325))
            self.screen.blit(smallFont.render("Normal Mode makes the enemies shoot at the standard rate.", -1, self.yellow),(15, 355))

            # expert button description
            self.screen.blit(smallFont.render("Expert Mode starts with 1 Life, 1 Bomb, and more points per kill.", -1, self.yellow),(15, 465))
            self.screen.blit(smallFont.render("Expert Mode makes the enemies shoot at a fast rate.", -1, self.yellow),(15, 495))
            pygame.display.update()

# GameLOOP -----------------------------------------------------------------------------------------------------------------------
    def run(self):
        highscoreCount = 1
        bombTimer = 20
        fpsCount = 0
        clock = pygame.time.Clock()
        for x in range(5):
            self.moveEnemiesDown()
        gameExit = False
        FPS = 60
        self.enemyCreate()
        while not gameExit:

            clock.tick(FPS)
            self.screen.fill(self.black)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
            for enemy in self.enemies:
                for enemy in enemy: #drawing the enemy and scaling the enemy
                    self.screen.blit(pygame.transform.scale(self.enemySprites[enemy[0]][self.animationOn], (35,35)), (enemy[1].x, enemy[1].y + 40))
            #drawing the player
            self.screen.blit(self.player, (self.playerPosX, self.playerPosY))
            if self.bullet:
                pygame.draw.rect(self.screen, (52,255,0), self.bullet)

            if self.bomb:
                self.bombAnimation()

            for Ebullet in self.enemyBullets:
                pygame.draw.rect(self.screen, self.white, Ebullet)
            for b in self.barrierParticles:
                pygame.draw.rect(self.screen, (100,255,100), b)


            if self.enemycount == 0:
                self.screen.blit(pygame.font.Font("game_font.ttf", 100).render("You Win!", -1, (52,255,0)), (100,70))
                self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("Press   to Play Again", -1, self.brightGreen),(50, 200))
                self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("P", -1, self.teal), (160, 200))
                self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("Press    to go to MainMenu", -1, self.brightGreen),(50, 250))
                self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("M", -1, self.teal), (160, 250))
                if highscoreCount == 1:
                    self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("Enter your name for the HighScore List", -1, self.brightGreen),(10, 450))
                    self.getUserName()
                    self.addHighScores()
                    highscoreCount = 0
                key = pygame.key.get_pressed()
                if key[K_p]:
                    self.playAgain()
                    self.run()
                if key[K_m]:
                    self.playAgain()
                    self.game_intro()
            elif self.lives > 0:
                self.bombUpdate()
                self.enemyBulletUpdate()
                self.bulletUpdate()
                self.enemyUpdate()
                self.playerUpdate()
                if bombTimer == 0:
                    bombTimer = 20
                    self.bombCount += 1
                if fpsCount == 60:
                    fpsCount = 0
                    bombTimer -= 1
                fpsCount += 1
            elif self.lives <= 0:
                self.screen.blit(pygame.font.Font("game_font.ttf", 100).render("GAME OVER!", -1, self.brightGreen), (100, 70))
                self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("Press   to Play Again", -1, self.brightGreen),(50,200))
                self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("P", -1, self.teal),(160, 200))
                self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("Press    to go to MainMenu", -1, self.brightGreen),(50,250))
                self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("M", -1, self.teal), (160, 250))
                if highscoreCount == 1:
                    self.screen.blit(pygame.font.Font("game_font.ttf", 50).render("Enter your name for the HighScore List", -1, self.brightGreen),(10, 450))
                    self.getUserName()
                    self.addHighScores()
                    highscoreCount = 0
                key = pygame.key.get_pressed()
                if key[K_p]:
                    self.playAgain()
                    self.run()
                if key[K_m]:
                    self.playAgain()
                    self.game_intro()
            self.screen.blit(self.font.render("Lives: {}".format(self.lives), -1, self.white), (0, 10))
            self.screen.blit(self.font.render("Score: {}".format(self.score), -1, self.white), (450, 10))
            self.screen.blit(self.font.render("Bombs: {}".format(self.bombCount), -1, self.white), (100, 10))
            self.screen.blit(self.font.render("Bomb Timer: {}".format(bombTimer), -1, self.white), (620, 10))
            pygame.display.update()




if __name__ == "__main__":
    MahyarSpaceInvaderI().game_intro()
    MahyarSpaceInvaderI().run()
    pygame.quit()
    quit()


