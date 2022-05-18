from sys import exit
from pprint import pprint
from time import sleep
from pygame import *
from pygame.locals import *
from itertools import cycle
from tools import *
from random import uniform

init()

vibrate = cycle([10, 5, .4, 7, 8, 3])

#====== Setup ======#
screen = display.set_mode()
width = screen.get_width()
height = screen.get_height()
clock = time.Clock()
display.set_caption("space shooter")
group = sprite.Group() # group of sprites
	# <Screen BackGround>
bg = image.load("./images/bg.png")
bg = transform.scale(bg, (width, height))

#====== Sprites ======#
	# <Player>
player = Sprite(
	"./images/player/player.png",
	(width/2, height-300),
	(16*5, 20*5),
	prop={
		"damage": 10,
		"score": 0
	}
)
	# <Player Projectile>
player_proj = Sprite(
	"./images/player/projectile.png",
	(0, 0),
	[20, 70]
)

	# <Enimy>
enimy = Sprite(
	"./images/enimy/enimy.png",
	(0, 0),
	(16*4, 20*4),
	speed=[0, 5]
)

	# <Rocks>
rock = Sprite(
	"./images/enimy/rock.png",
	(0, 0),
	(16*3, 16*3)
)
#====== GUI ======#
	# <Move Buttons>
right_button = Sprite(
	"./images/gui/right.png",
	(30, height-(20*7+30)),
	(20*7, 20*7)
)
left_button = Sprite(
	"./images/gui/left.png",
	((20*7+40), height-(20*7+30)),
	(20*7, 20*7)
)
 # <Shoot Button For player_proj>
shoot_button = Sprite(
	"./images/gui/shoot.png",
	(width-(20*7+30), height-(20*7+30)),
	(20*7, 20*7)
)

	# <Score>
font = font.Font(None, 70)
score = font.render(f"Score: {player.prop['score']}", True, "White")
score_rect = score.get_rect()
score_rect.center = [width/2, 30]

	# <Damage>
damage = font.render(f"Damage: {player.prop['damage']}", True, "Red")
damage_rect = damage.get_rect()
damage_rect.x = 30
damage_rect.y = 70

######Add Sprites And GUI To Group######
sprites = [
	player,
	right_button,
	left_button,
	shoot_button
]
for sp in sprites:
	group.add(sp)

#====== Main Loop ======#
shoot = 0
rocking = 0 # yeh
while True:
	for ev in event.get():
		if ev.type == QUIT:
			quit()
			exit()
	screen.fill((0, 0, 0))
	
	# <Player Controls>
	mouvment_cycle = cycle([15, 14, 13, 16])
	if right_button.clicked():
		player.add_x(-next(mouvment_cycle))
		if player.rect.left < 0:
			player.rect.left = 0
	if left_button.clicked():
		player.add_x(next(mouvment_cycle))
		if player.rect.right > width:
			player.rect.right  = width
	
		# <Shoot Projectile System>
	if shoot_button.clicked() and shoot == 0:
		name = player_proj.copy()
		name.set_pos(player.rect.center)
		name.add_x(-10)
		player_proj.clones.append(name)
		shoot += 6
	if shoot > 0:
		shoot -= 1
	for i in player_proj.clones:
		group.add(i)
		i.add_y(-14)
		if i.rect.top < 0:
			i.kill()
			player_proj.clones.remove(i)
			group.remove(i)
	
	if rocking == 0:
		c = rock.copy()
		rock.set_pos((
			uniform(0, width-c.rect.size[0]),
			0
		))
		rock.clones.append(c)
		rocking += 100	
	if rocking > 0:
		rocking -= 1
	for i in rock.clones:
		group.add(i)
		i.add_y(5)
		if i.rect.bottom >= height or i.rect.left >= width:
			i.kill()
			rock.clones.remove(i)
			group.remove(i)
		if i.colliderect(player):
			player.prop["damage"] += 2
			player.prop["score"] += round(uniform(200, 300))
			i.kill()
			try:rock.clones.remove(i)
			except:
				pass
			group.remove(i)
	
	
	
	if len(enimy.clones) <= 10:
		c = enimy.copy()
		c.set_pos((
			uniform(0, width-c.rect.size[0]),
			uniform(0, 700)
		))
		c.rotate(180)
		if not c.colliderect(enimy.clones):
			enimy.clones.append(c)
	
	for i in enimy.clones:
		group.add(i)
		enimy.speed[0] += .00009
		enimy.speed[1] = next(vibrate)
		i.move()
		if i.rect.bottom >= height or i.rect.left >= width:
			i.kill()
			enimy.clones.remove(i)
			group.remove(i)
		if i.colliderect(player_proj.clones):
			i.kill()
			enimy.clones.remove(i)
			group.remove(i)
			player.prop["score"] += round(uniform(100, 200))
		if i.colliderect(player):
			player.prop["damage"] -= 1
			i.kill()
			try:enimy.clones.remove(i)
			except:
				pass
			group.remove(i)
	
	if player.prop["damage"] == 0:
		quit()
		exit()
	
	# <Render>
	bg_rect = bg.get_rect()
	bg_rect.x = next(vibrate)
	bg_rect.y = next(vibrate)
	screen.blit(bg, bg_rect)
	group.draw(screen)
	score = font.render(f"Score: {player.prop['score']}", True, "White")
	screen.blit(score, score_rect)
	damage = font.render(f"Damage: {player.prop['damage']}", True, "Red")
	screen.blit(damage, damage_rect)
	display.update()
	display.flip()
	clock.tick(120)
