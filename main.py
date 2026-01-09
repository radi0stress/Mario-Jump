# Prepare File and Aset
from pygame import*
from random import choice
LEBAR = 700
TINGGI = 500
window = display.set_mode((LEBAR, TINGGI))
display.set_caption("Mario Jump")
bg = transform.scale(image.load('bg.jpg'), [LEBAR, TINGGI])
gravitasi = 0.9
# Music
mixer.init()
mixer.music.load('sound.ogg')
mixer.music.play()
jump = mixer.Sound('jump.ogg')
jump.set_volume(0.6)

# GameSprite Class
class GameSprite(sprite.Sprite):
  def __init__(self, img, x, y, w, h):
      super().__init__()
      self.image = transform.scale(image.load(img), (w, h))  
      self.rect = self.image.get_rect()
      self.rect.x = x 
      self.rect.y = y

  def reset(self):
      window.blit(self.image, (self.rect.x, self.rect.y))
# Player Class
class Player(GameSprite):
    def __init__(self, img, x, y, w, h):
        super().__init__(img, x, y, w, h)
        self.vel_y = 0
        self.on_ground = False
        self.jump_power = 23
    def update(self):
        keys = key.get_pressed()
        if keys[K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            jump.play()
        self.vel_y += gravitasi
        self.rect.y += self.vel_y
        if self.rect.bottom >= TINGGI - 75:
            self.rect.bottom = TINGGI - 75
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
# Enemy Class
class Enemy(GameSprite):
    def __init__(self, img, x, y, w, h):
        super().__init__(img, x, y, w, h)
    # Enemy update
    def update(self):
        global lost, score
        self.rect.x -= 6
        if self.rect.x < -50:
            self.rect.x = 800
            score += 1
# Coin class
class Coin(GameSprite):
    def __init__(self, img, x, y, w, h):
        super().__init__(img, x, y, w, h)
    def update(self):
        self.rect.x -= 6
        if self.rect.x < -50:
            self.reset_pos()
    def reset_pos(self):
        self.rect.x = 800
        self.rect.y = choice([330, 350, 370])

# Object
player = Player('player.png', 100, 200, 75, 75)
enemy1 = Enemy('enemy1.png', 600, 355, 80, 80)
coin = Coin('coin.png', 900, 350, 40, 40)

list_enemy = [enemy1]
cur_enemy = choice(list_enemy)
# Enemy Group
enemys = sprite.Group()
enemys.add(cur_enemy)
coins = sprite.Group()
coins.add(coin)

# Font
font.init()
font2 = font.Font(None, 40) #score
font1 = font.Font(None, 72)
font3 = font.Font(None, 30) #small
lose_t = font1.render('Try Again ?', True, (255, 0, 0))
press_s = font3.render('Press Space for Try again and Press Q for Quit', True, (255, 193, 50))
next_game = font1.render('See you next game !', True, (26, 110, 255))
score = 0
lost = 0
quit_game = False

#FPS
clock = time.Clock()
FPS = 60
stop = False
# Loop Game
run = True
while run:
    clock.tick(FPS)
    # Event
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not stop:
        if cur_enemy.rect.x < -40:
            cur_enemy = choice(list_enemy)
            cur_enemy.rect.x = 800
        # Background
        window.blit(bg, (0, 0))
        # Update
        player.update()
        cur_enemy.update()
        # Draw
        player.reset()
        cur_enemy.reset()
        # Coin
        coin.update()
        coin.reset()
        # Text
        score_t = font2.render('Score : ' + str(score), True, (0, 0, 0))
        window.blit(score_t, (135, 40))
        # Win / Lose
        if score >= 10:
            win_t = font1.render('Congratulation!', True, (26, 110, 255))
            window.blit(win_t, (120, 270))
            mixer.music.stop()
            stop = True
        # Collision detect
        if sprite.spritecollide(player, enemys, False):
            mixer.music.stop()
            stop = True
        if sprite.spritecollide(player, coins, True):
            score += 1
            coin.reset_pos()
            coins.add(coin)
    if stop and score < 10:
        window.blit(lose_t, (200, 200))
        window.blit(press_s, (120, 270))
        keys = key.get_pressed()
        if keys[K_SPACE]:
            stop = False
            enemy1.rect.x = 800
            score = 0
            mixer.music.play()
        if keys[K_q]:
            quit_game = True
        if quit_game:
            window.blit(bg, (0, 0))
            window.blit(next_game, (110, 270))
    if stop and score >= 10:
        window.blit(bg, (0, 0))
        win_t = font1.render('Congratulation!', True, (26, 110, 255))
        window.blit(win_t, (120, 270))
        mixer.music.stop()
    display.update()

