# Samurai X Adventure

# Author : Caio Cabral
# Date : Tuesday, 10 March, 2026

import random
import pygame

from objects import Ground, Samurai, Obstacle, Cloud, Bird, Star

pygame.init()
SCREEN = WIDTH, HEIGHT = (600, 200)
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock()
FPS = 60

# COLORS *********************************************************************

WHITE = (225,225,225)
BLUE = (36, 159, 222)

# IMAGES *********************************************************************

start_img = pygame.image.load('assets/start_img.png')
start_img = pygame.transform.scale(start_img, (60, 64))

game_over_img = pygame.image.load('assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200, 36))

replay_img = pygame.image.load('assets/replay.png')
replay_img = pygame.transform.scale(replay_img, (40, 36))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 - 20
replay_rect.y = 100

numbers_img = pygame.image.load('assets/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

# SOUNDS *********************************************************************

jump_fx = pygame.mixer.Sound('assets/sounds/jump-song.wav')
die_fx = pygame.mixer.Sound('assets/sounds/die-song.wav')
checkpoint_fx = pygame.mixer.Sound('assets/sounds/checkPoint-song.wav')

# OBJECTS & GROUPS ***********************************************************

ground = Ground()
samurai = Samurai(50, 160)

obstacle_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()

# FUNCTIONS ******************************************************************

def reset():
	global counter, SPEED, score, high_score

	if score and score >= high_score:
		high_score = score

	counter = 0
	SPEED = 5
	score = 0

	obstacle_group.empty()
	bird_group.empty()
	cloud_group.empty()
	stars_group.empty()

	samurai.reset()

# CHEATCODES *****************************************************************

# GODMODE -> immortal jutsu ( can't die )
# DAYMODE -> Swap between day and night
# LYAGAMI -> automatic jump and duck
# IAMRICH -> add 10,000 to score
# HISCORE -> highscore is 99999
# SPEEDUP -> increase speed by 2

keys = []
GODMODE = False
DAYMODE = False
LYAGAMI = False

# VARIABLES ******************************************************************

counter = 0
enemy_time = 100
cloud_time = 500
stars_time = 175

SPEED = 5
jump = False
duck = False

score = 0
high_score = 0

start_page = True
mouse_pos = (-1, -1)

running = True
while running:
	jump = False
	if DAYMODE:
		win.fill(WHITE)
	else:
		win.fill(BLUE)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False

			if event.key == pygame.K_SPACE:
				if start_page:
					start_page = False
				elif samurai.alive:
					jump = True
					jump_fx.play()
				else:
					reset()

			if event.key == pygame.K_UP:
				jump = True
				jump_fx.play()

			if event.key == pygame.K_DOWN:
				duck = True

			key = pygame.key.name(event.key)
			keys.append(key)
			keys = keys[-7:]
			if ''.join(keys).upper() == 'GODMODE':
				GODMODE = not GODMODE

			if ''.join(keys).upper() == 'DAYMODE':
				DAYMODE = not DAYMODE

			if ''.join(keys).upper() == 'LYAGAMI':
				LYAGAMI = not LYAGAMI

			if ''.join(keys).upper() == 'SPEEDUP':
				SPEED += 2

			if ''.join(keys).upper() == 'IAMRICH':
				score += 10000

			if ''.join(keys).upper() == 'HISCORE':
				high_score = 99999

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
				jump = False

			if event.key == pygame.K_DOWN:
				duck = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = event.pos

		if event.type == pygame.MOUSEBUTTONUP:
			mouse_pos = (-1, -1)

	if start_page:
		win.blit(start_img, (50, 100))
	else:
		if samurai.alive:
			counter += 1
			if counter % int(enemy_time) == 0:
				if random.randint(1, 10) == 5:
					y = random.choice([100, 130])
					bird = Bird(WIDTH, y)
					bird_group.add(bird)
				else:
					type = random.randint(1, 14)
					obstacle = Obstacle(type)
					obstacle_group.add(obstacle)

			if counter % cloud_time == 0:
				y = random.randint(40, 100)
				cloud = Cloud(WIDTH, y)
				cloud_group.add(cloud)

			if counter % stars_time == 0:
				type = random.randint(1, 3)
				y = random.randint(40, 100)
				star = Star(WIDTH, y, type)
				stars_group.add(star)

			if counter % 100 == 0:
				SPEED += 0.1
				enemy_time -= 0.5

			if counter % 5 == 0:
				score += 1

			if score and score % 100 == 0:
				checkpoint_fx.play()

			if not GODMODE:
				for obstacle in obstacle_group:
					if LYAGAMI:
						dx = obstacle.rect.x - samurai.rect.x
						if 0 <= dx <= (70 + (score//100)):
							jump = True

					if pygame.sprite.collide_mask(samurai, obstacle):
						SPEED = 0
						samurai.alive = False
						die_fx.play()

				for obstacle in bird_group:
					if LYAGAMI:
						dx = bird.rect.x - samurai.rect.x
						if 0 <= dx <= 70:
							if samurai.rect.top <= bird.rect.top:
								jump = True
							else:
								duck = True
						else:
							duck = False

					if pygame.sprite.collide_mask(samurai, bird):
						SPEED = 0
						samurai.alive = False
						die_fx.play()

		ground.update(SPEED)
		ground.draw(win)
		cloud_group.update(SPEED-3, samurai)
		cloud_group.draw(win)
		stars_group.update(SPEED-3, samurai)
		stars_group.draw(win)
		obstacle_group.update(SPEED, samurai)
		obstacle_group.draw(win)
		bird_group.update(SPEED-1, samurai)
		bird_group.draw(win)
		samurai.update(jump, duck)
		samurai.draw(win)

		string_score = str(score).zfill(5)
		for i, num in enumerate(string_score):
			win.blit(numbers_img, (520+11*i, 10), (10*int(num), 0, 10, 12))

		if high_score:
			win.blit(numbers_img, (425, 10), (100, 0, 20, 12))
			string_score = f'{high_score}'.zfill(5)
			for i, num in enumerate(string_score):
				win.blit(numbers_img, (455+11*i, 10), (10*int(num), 0, 10, 12))

		if not samurai.alive:
			win.blit(game_over_img, (WIDTH//2-100, 55))
			win.blit(replay_img, replay_rect)

			if replay_rect.collidepoint(mouse_pos):
				reset()

	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()