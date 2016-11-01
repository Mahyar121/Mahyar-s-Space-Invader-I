'''
Mahyar Haji Babaie
mahyarhajibabaie@csu.fullerton.edu
game page
'''
import pygame
from pygame.locals import *
import random
pygame.init()
from time import sleep
#class for the game Mahyar's Space Invader I
class MahyarSpaceInvaderI:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.smallText = pygame.font.Font("game_font.ttf", 40)
        self.white = (255,255,255)
        self.teal = (0, 200, 255)
        self.green = (0, 200, 0)
        self.brightGreen = (0, 255, 0)
        self.red = (255, 0, 0)
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
        #sets the display resolution
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        #the enemy sprites
        self.enemySprites = {
            0:[pygame.image.load("e1_0.png").convert(), pygame.image.load("e1_1.png").convert()],
            1:[pygame.image.load("e2_0.png").convert(), pygame.image.load("e2_1.png").convert()],
            2:[pygame.image.load("e3_0.png").convert(), pygame.image.load("e3_1.png").convert()],
        }
        #the player sprite
        self.player = pygame.image.load("player.png").convert()
        pygame.display.set_icon(self.player)
        self.animationOn = 0
        self.direction = 1
        self.enemySpeed = 10
        self.lastEnemyMove = 0
        self.playerPosX = 400
        self.playerPosY = 550
        self.bullet = None
        self.bullets = []
        self.enemies = []
        self.barrierParticles = []
        self.enemycount = 50
        startY = 50
        startX = 50

        #positioning the enemy sprites in the rows
        for rows in range(5):
            out = []
            if rows < 1:
                enemy = 2
            elif rows < 3:
                enemy = 1
            else:
                enemy = 0
            for columns in range(10):
                out.append((enemy,pygame.Rect(startX * columns, startY * rows, 35, 35)))
            self.enemies.append(out)
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

    def enemyUpdate(self):
        if not self.lastEnemyMove:
            for enemy in self.enemies:
                for enemy in enemy:
                    enemy = enemy[1]
                    #if enemy collides with player then the player loses a life and resets position of player
                    if enemy.colliderect(pygame.Rect(self.playerPosX, self.playerPosY, self.player.get_width(), self.player.get_height())):
                        self.lives -= 1
                        self.resetPlayer()
                    #the x position of the enemy
                    enemy.x += self.enemySpeed * self.direction
                    self.lastEnemyMove = 25
                    # if the enemy is in the map, move them down
                    if enemy.x >= 750 or enemy.x <= 0:
                        self.moveEnemiesDown()
                        self.direction *= -1

                    chance = random.randint(0, 1000)
                    #how often the enemy shoots
                    if chance > self.chance:
                        self.bullets.append(pygame.Rect(enemy.x, enemy.y, 5, 15))
                        self.score += 10
            if self.animationOn:
                self.animationOn -= 1
            else:
                self.animationOn += 1
        else:
            self.lastEnemyMove -= 1
    #moves enemy units down
    def moveEnemiesDown(self):
        for enemy in self.enemies:
            for enemy in enemy:
                enemy = enemy[1]
                enemy.y += 20

    #handles the buttons for the player
    def playerUpdate(self):
        key = pygame.key.get_pressed()
        if key[K_LEFT] and self.playerPosX > 0:
            self.playerPosX -= 5
        elif key[K_RIGHT] and self.playerPosX < self.display_width - self.player.get_width():
            self.playerPosX += 5
        if key[K_SPACE] and not self.bullet:
            self.bullet = pygame.Rect(self.playerPosX + self.player.get_width() / 4, self.playerPosY - 15, 5, 10)


    def bulletUpdate(self):
        for i, enemy in enumerate(self.enemies):
            for j, enemy in enumerate(enemy):
                enemy = enemy[1]
                #if a bullet hits an enemy you get 100 points
                if self.bullet and enemy.colliderect(self.bullet):
                    self.enemies[i].pop(j)
                    self.enemycount -= 1
                    self.bullet = None
                    self.chance -= 1
                    self.score += 100
        if self.bullet:
            self.bullet.y -= 10
            if self.bullet.y < 0:
                self.bullet = None

        for x in self.bullets:
            #speed of bullet
            x.y += 7
            #if bullets off the screen then remove it
            if x.y > 600:
                self.bullets.remove(x)
            # if bullets hits the player then remove a life and reset him
            if x.colliderect(pygame.Rect(self.playerPosX, self.playerPosY, self.player.get_width(), self.player.get_height())):
                self.lives -= 1
                self.bullets.remove(x)
                self.resetPlayer()

        for b in self.barrierParticles:
            check = b.collidelist(self.bullets)
            if check != -1:
                self.barrierParticles.remove(b)
                self.bullets.pop(check)
                self.score += 10
            elif self.bullet and b.colliderect(self.bullet):
                self.barrierParticles.remove(b)
                self.bullet = None
                self.score += 10

    def resetPlayer(self):
        self.playerPosX = 400

    def text_objects(self, text, font):
        #white font
        textSurface = font.render(text, True, (255,255,255))
        return textSurface, textSurface.get_rect()

    def gameIntroButton(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #Quit button
        if 275 + 260 > mouse[0] > 275 and 455 + 50 > mouse[1] > 455:
            self.buttonBorder(self.white, 270,450,270,60)
            self.buttonBorder(self.brightGreen,275,455,260,50)
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            self.buttonBorder(self.white,270,450,270,60)
            self.buttonBorder(self.green,275,455,260,50)
        self.textButton("Quit",275,455,260,50)
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
        #Play button
        if 275 + 260 > mouse[0] > 275 and 155 + 50 > mouse[1] > 155:
            self.buttonBorder(self.white,270,150,270,60)
            self.buttonBorder(self.brightGreen, 275,155,260,50)
            if click[0] == 1:
                self.run()
        else:
            self.buttonBorder(self.white, 270, 150, 270, 60)
            self.buttonBorder(self.green, 275, 155, 260, 50)
        self.textButton("Play",275,155,260,50)

    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #black screen
            self.screen.fill((0,0,0))
            bigText = pygame.font.Font("game_font.ttf", 60)
            textSurface, textRectange = self.text_objects("Mahyar's Space Invader I", bigText)
            textRectange.center = ((self.display_width/2), (self.display_height/15))
            self.screen.blit(textSurface, textRectange)
            #shows the buttons on the game menu screen
            self.gameIntroButton()
            pygame.display.update()
            clock = pygame.time.Clock()
            clock.tick(15)

    def buttonBorder(self, color, x, y, w, h):
        pygame.draw.rect(self.screen, color, (x, y, w, h))

    def textButton(self, txt, x, y, w, h,):
        textSurface, textRectangle = self.text_objects(txt, self.smallText)
        textRectangle.center = ((x + (w/2)), (y + (h/2)))
        self.screen.blit(textSurface, textRectangle)


    def controlButtons(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #quit button
        if 475 + 260 > mouse[0] > 475 and 545 + 40 > mouse[1] > 545:
            self.buttonBorder(self.white,470,540,270,50)
            self.buttonBorder(self.brightGreen,475,545,260,40)
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            self.buttonBorder(self.white, 470, 540, 270, 50)
            self.buttonBorder(self.green, 475, 545, 260, 40)
        self.textButton("Quit",475,545,260,40)
        #back button
        if 80 + 260 > mouse[0] > 80 and 545 + 40 > mouse[1] > 545:
            self.buttonBorder(self.white, 75, 540, 270, 50)
            self.buttonBorder(self.brightGreen, 80, 545, 260, 40)
            if click[0] == 1:
                self.game_intro()
        else:
            self.buttonBorder(self.white, 75, 540, 270, 50)
            self.buttonBorder(self.green, 80, 545, 260, 40)
        self.textButton("Back",80,545,260,40)
        # Control BUTTONS
        # Move Left
        self.buttonBorder(self.red,75,150,270,50)
        self.buttonBorder(self.teal,80,155,260,40)
        self.textButton("Move Left:",80,155,260,40)
        # left arrow
        self.buttonBorder(self.red, 475, 150, 270, 50)
        self.buttonBorder(self.teal, 480, 155, 260, 40)
        self.textButton("Left Arrow", 480, 155, 260, 40)
        # Move Right
        self.buttonBorder(self.red, 75, 250, 270, 50)
        self.buttonBorder(self.teal, 80, 255, 260, 40)
        self.textButton("Move Right:", 80, 255, 260, 40)
        # right arrow
        self.buttonBorder(self.red, 475, 250, 270, 50)
        self.buttonBorder(self.teal, 480, 255, 260, 40)
        self.textButton("Right Arrow", 480, 255, 260, 40)
        # Attack
        self.buttonBorder(self.red, 75, 350, 270, 50)
        self.buttonBorder(self.teal, 80, 355, 260, 40)
        self.textButton("Attack:", 80, 355, 260, 40)
        # Space Bar
        self.buttonBorder(self.red, 475, 350, 270, 50)
        self.buttonBorder(self.teal, 480, 355, 260, 40)
        self.textButton("SpaceBar", 480, 355, 260, 40)

    def controlsPage(self):
        controls = True
        while controls:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # black screen
            self.screen.fill((0, 0, 0))
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


    def run(self):

        clock = pygame.time.Clock()
        for x in range(5):
            self.moveEnemiesDown()
        gameExit = False
        FPS = 60
        while not gameExit:

            clock.tick(FPS)
            self.screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
            for enemy in self.enemies:
                for enemy in enemy: #drawing the enemy and scaling the enemy
                    self.screen.blit(pygame.transform.scale(self.enemySprites[enemy[0]][self.animationOn], (35,35)), (enemy[1].x, enemy[1].y))
            #drawing the player
            self.screen.blit(pygame.transform.scale(self.player, (50,50)), (self.playerPosX, self.playerPosY))
            if self.bullet:
                pygame.draw.rect(self.screen, (52,255,0), self.bullet)
            for bullet in self.bullets:
                pygame.draw.rect(self.screen, (255,255,255), bullet)
            for b in self.barrierParticles:
                pygame.draw.rect(self.screen, (100,255,100), b)

            if self.enemycount == 0:
                self.screen.blit(pygame.font.Font("game_font.ttf", 100).render("You Win!", -1, (52,255,0)), (100,200))
            elif self.lives > 0:
                self.bulletUpdate()
                self.enemyUpdate()
                self.playerUpdate()
            elif self.lives <= 0:
                self.screen.blit(pygame.font.Font("game_font.ttf", 100).render("You Lose!", -1, (52,255,0)), (100, 200))
            self.screen.blit(self.font.render("Lives: {}".format(self.lives), -1, (255, 255, 255)), (20, 10))
            self.screen.blit(self.font.render("Score: {}".format(self.score), -1, (255, 255, 255)), (400, 10))
            pygame.display.update()




if __name__ == "__main__":
    MahyarSpaceInvaderI().game_intro()
    MahyarSpaceInvaderI().run()
    pygame.quit()
    quit()




