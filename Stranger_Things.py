from moviepy.editor import *
import pygame
import time
pygame.init()

# Window
win = pygame.display.set_mode((500,480))
pygame.display.set_caption('Stranger Things')
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)

# Images Jim_Hopper
walkRight = [pygame.image.load('r1.png'), pygame.image.load('r2.png'), pygame.image.load('r3.png'), pygame.image.load('r4.png'), pygame.image.load('r5.png'), pygame.image.load('r6.png'), pygame.image.load('r7.png'), pygame.image.load('r8.png'), pygame.image.load('r9.png')]
walkLeft = [pygame.image.load('l1.png'), pygame.image.load('l2.png'), pygame.image.load('l3.png'), pygame.image.load('l4.png'), pygame.image.load('l5.png'), pygame.image.load('l6.png'), pygame.image.load('l7.png'), pygame.image.load('l8.png'), pygame.image.load('l9.png')]
jim_hopper_dead = [pygame.image.load('d1.png'), pygame.image.load('d2.png'), pygame.image.load('d3.png'), pygame.image.load('d4.png'), pygame.image.load('d5.png'), pygame.image.load('d6.png')]
char  = pygame.image.load('standing.png')
hearts = pygame.image.load('heart.png')
broken_heart = pygame.image.load('broken_heart.png')

# Backgroud images
start = pygame.image.load('start_button.png')
bg = pygame.image.load('back.png')
bg2 = pygame.image.load('bg2.png')
bgwin = pygame.image.load('bg_win.png')
bglose = pygame.image.load('bglose.png')

# Intro video
clip = VideoFileClip('intro.mp4')
clip1 = clip.resize((480,500))

# Sounds
collisionSound = pygame.mixer.Sound('collision.mp3')
jumpSound = pygame.mixer.Sound('jump.mp3')
bulletSound = pygame.mixer.Sound('bullet.mp3')      
hitSound = pygame.mixer.Sound('hit.mp3')
winSound = pygame.mixer.Sound('win.mp3')
loseSound = pygame.mixer.Sound('lose.mp3')            
music = pygame.mixer.music.load('music.mp3')      
pygame.mixer.music.play(-1)                        

# Timer
clock = pygame.time.Clock()

# score = 0

    
# Hero Jim Hopper                                                    
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        self.dead = jim_hopper_dead 
     
 # Player movement   
    def draw(self, win):
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
                
            if not(self.standing):    
                if self.left:
                    win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                    self.walkCount +=1
                elif self.right:
                    win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                    self.walkCount += 1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            
            # Player healthbar and hitbox
            pygame.draw.rect(win, (255,0,0), (390, 10, 100, 10))
            pygame.draw.rect(win, (0,255,0), (390, 10, 100 -(10 * (10 - self.health)), 10))       
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            win.blit(hearts, (483, 8)) 
            #pygame.draw.rect(win, (255, 0, 0 ), self.hitbox, 2)
    
# Player health function    
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 300
        self.y = 410
        self.walkCount = 0
        collisionSound.play()
        win.blit(broken_heart, (self.hitbox[0]+5, self.hitbox[1]-18))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(3)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                
                    i = 301
                    pygame.quit()  
        if self.health > 0:
            self.health -= 1
        else:
            for i in jim_hopper_dead:
                win.blit(i,(self.x,self.y))
                pygame.display.update()
                pygame.time.delay(100)
                win.blit(bglose,(0,0))
                loseSound.play()
            self.visible = False
            time.sleep(4)
            pygame.quit()

# Player bullets            
class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing       
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

# Enemy Demogorgon
class enemy(object):
    walkRight = [pygame.image.load('re1.png'), pygame.image.load('re2.png'), pygame.image.load('re3.png'), pygame.image.load('re4.png'), pygame.image.load('re5.png'), pygame.image.load('re6.png'), pygame.image.load('re7.png'), pygame.image.load('re8.png'), pygame.image.load('re9.png'), pygame.image.load('re10.png'), pygame.image.load('re11.png')]
    walkLeft = [pygame.image.load('le1.png'), pygame.image.load('le2.png'), pygame.image.load('le3.png'), pygame.image.load('le4.png'), pygame.image.load('le5.png'), pygame.image.load('le6.png'), pygame.image.load('le7.png'), pygame.image.load('le8.png'), pygame.image.load('le9.png'), pygame.image.load('le10.png'), pygame.image.load('le11.png')]
    demogorgon_dead = [pygame.image.load('de1.png'), pygame.image.load('de2.png'), pygame.image.load('de3.png'), pygame.image.load('de4.png'), pygame.image.load('de5.png'), pygame.image.load('de6.png')]
    
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 10
        self.visible = True
        
# Enemy movement    
    def draw(self, win):
        self.move()
        if self.visible: 
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
                
            if self.vel > 0 :
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            
            # Enemy helthbar and hitbox    
            pygame.draw.rect(win, (255,0,0), (10, 10, 100, 10))
            pygame.draw.rect(win, (0,255,0), (10, 10, 100 -(10 * (10 - self.health)), 10))   
            self.hitbox = (self.x + 20, self.y, 28, 60)
            win.blit(hearts, (2, 8))
            #pygame.draw.rect(win, (255, 0, 0 ), self.hitbox, 2)
    
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    
# Enemy health function            
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            for i in self.demogorgon_dead:
                win.blit(i,(self.x, self.y))
                pygame.display.update()
                pygame.time.delay(100)
                win.blit(bgwin,(0,0))    
            self.visible = False
            winSound.play()
            time.sleep(4)
            pygame.quit()
                
# Enemy collison function   
    def colision(self):
        self.x = 100
        self.y = 410
        i = 0
        while i < 100:
            pygame.time.delay(0)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit() 

# Start button                    
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
                   
        win.blit(self.image, (self.rect.x, self.rect.y))
        return action
        
start_button = Button(160,280, start)         

# Intro window
def drawGameWindow():
    win.blit(bg, (0,0))
    if start_button.draw():
         clip1 = clip.resize((480,500))
         clip1.preview()
         clip1.close()
          
    pygame.display.update()
             
# Gameplay window           
def redrawGameWindow():
    win.blit(bg2, (0,0))
    #text = font.render('Score: ' + str(score), 1, (255,0,0))
    #win.blit(text, (190, 10))
    jim_hopper.draw(win)
    demogorgon.draw(win)
    for bullet in bullets:
        bullet.draw(win)
  
    pygame.display.update()
        
    
# Main loop
font = pygame.font.SysFont('comicsans', 30, True)       
jim_hopper = player(300, 410, 64, 64)
demogorgon = enemy(100, 410, 64, 64, 300)
shootLoop = 0
bullets = []
run = True

while run:
    clock.tick(27)
    
    if demogorgon.visible:    
     if jim_hopper.hitbox[1] < demogorgon.hitbox[1] + demogorgon.hitbox[3] and jim_hopper.hitbox[1] + jim_hopper.hitbox[3] > demogorgon.hitbox[1]:
         if jim_hopper.hitbox[0] + jim_hopper.hitbox[2] > demogorgon.hitbox[0] and jim_hopper.hitbox[0] < demogorgon.hitbox[0] + demogorgon.hitbox[2]:
             jim_hopper.hit()
             demogorgon.colision()
             # score -= 5
             
     if shootLoop > 0:
         shootLoop += 1
     if shootLoop > 3:
         shootLoop = 0
         
     for event in pygame.event.get():
         if event.type == pygame.QUIT:
             run = False
             
     for bullet in bullets:
         if bullet.y - bullet.radius < demogorgon.hitbox[1] + demogorgon.hitbox[3] and bullet.y + bullet.radius > demogorgon.hitbox[1]:
             if bullet.x + bullet.radius > demogorgon.hitbox[0] and bullet.x - bullet.radius < demogorgon.hitbox[0] + demogorgon.hitbox[2]:
                 hitSound.play()
                 demogorgon.hit()
                 # score += 1
                 bullets.pop(bullets.index(bullet))
         
         if bullet.x < 500 and bullet.x > 0:
             bullet.x += bullet.vel
         else:
             bullets.pop(bullets.index(bullet))
             
     keys = pygame.key.get_pressed()
      
     if keys[pygame.K_SPACE] and shootLoop == 0:
         bulletSound.play()
         if jim_hopper.left:
             facing = -1
         else:
             facing = 1
             
         if len(bullets) < 5:
            bullets.append(projectile(round(jim_hopper.x + jim_hopper.width //2), round(jim_hopper.y + jim_hopper.height//2), 6, (196,174,173), facing))
          
         shootLoop = 1     
       
     if keys[pygame.K_LEFT] and jim_hopper.x > jim_hopper.vel:
         jim_hopper.x -= jim_hopper.vel
         jim_hopper.left = True
         jim_hopper.right = False
         jim_hopper.standing = False
         
     elif keys[pygame.K_RIGHT] and jim_hopper.x < 500 - jim_hopper.width - jim_hopper.vel:
         jim_hopper.x += jim_hopper.vel
         jim_hopper.right = True
         jim_hopper.left = False
         jim_hopper.standing = False
         
     else:
         jim_hopper.standing = True
         jim_hopper.walkCount = 0
         
     if not(jim_hopper.isJump):        
         if keys[pygame.K_UP]:
             jumpSound.play()
             jim_hopper.isJump = True
             jim_hopper.left = False
             jim_hopper.right = False
             jim_hopper.walkCount = 0
             
             
     else:
         if jim_hopper.jumpCount >= -10:
             neg = 1
             if jim_hopper.jumpCount < 0:
                 neg = -1
             jim_hopper.y -= (jim_hopper.jumpCount ** 2) * 0.5 * neg
             jim_hopper.jumpCount -= 1
         else:
             jim_hopper.isJump = False
             jim_hopper.jumpCount = 10
             
    #drawGameWindow()
    redrawGameWindow()   
        
pygame.quit()

