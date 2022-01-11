import pygame
import math
pygame.font.init()

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER_WIDTH = 10
BORDER = pygame.Rect((WIDTH // 2) - BORDER_WIDTH, 0, BORDER_WIDTH * 2, HEIGHT)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55 * 2, 40 * 2
YELLOW_SPACESHIP_IMAGE = pygame.image.load('spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
RED_SPACESHIP_IMAGE = pygame.image.load('spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
SPACE = pygame.transform.scale(pygame.image.load('space.png'), (WIDTH, HEIGHT))
HEALTH_FONT = pygame.font.SysFont("FantasqueSansMono Nerd Font", 45)
WINNER_FONT = pygame.font.SysFont("FantasqueSansMono Nerd Font", 100)
pygame.display.set_caption("PygameTutorial")

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, current_round, round_length, frames_since_last):
	WIN.blit(SPACE, (0, 0))
	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
	WIN.blit(RED_SPACESHIP, (red.x, red.y))
	pygame.draw.rect(WIN, (0, 0, 0), BORDER)

	for bullet in red_bullets:
		pygame.draw.rect(WIN, (255, 0, 0), bullet)

	for bullet in yellow_bullets:
		pygame.draw.rect(WIN, (255, 255, 0), bullet)

	red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, (255, 0, 0))
	yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, (255, 255, 0))
	round_text = HEALTH_FONT.render(("Round " + str(current_round)), 1, (0, 255, 0))
	length_text = HEALTH_FONT.render(("Time Remaining in Round: " + str(int((round_length // 60) - (frames_since_last // 60))) + " seconds"), 1, (0, 255, 0))
	WIN.blit(round_text, (WIDTH // 2 - round_text.get_width() // 2, 30))
	WIN.blit(length_text, (WIDTH // 2 - length_text.get_width() // 2, 40 + round_text.get_height()))
	WIN.blit(red_health_text, (20, 20))
	WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 20, 20))
	pygame.display.update()

def handle_input(ship, keys, arrow, VELOCITY):
	if (arrow): # yellow + right
		if (keys[pygame.K_LEFT] and ship.x > BORDER.x + BORDER.width):
			ship.x -= VELOCITY
		if (keys[pygame.K_RIGHT] and ship.x + ship.width < WIDTH):
			ship.x += VELOCITY
		if (keys[pygame.K_UP] and ship.y > 0):
			ship.y -= VELOCITY
		if (keys[pygame.K_DOWN] and ship.y + ship.height < HEIGHT):
			ship.y += VELOCITY
	if (not arrow): # red + left
		if (keys[pygame.K_a] and ship.x > 0):
			ship.x -= VELOCITY
		if (keys[pygame.K_d] and ship.x + ship.width < BORDER.x):
			ship.x += VELOCITY
		if (keys[pygame.K_w] and ship.y > 0):
			ship.y -= VELOCITY
		if (keys[pygame.K_s] and ship.y + ship.height < HEIGHT):
			ship.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red, BULLET_VELOCITY):
	for bullet in yellow_bullets:
		bullet.x -= BULLET_VELOCITY
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		elif bullet.x < 0:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x += BULLET_VELOCITY
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x > WIDTH:
			red_bullets.remove(bullet)
		
def draw_winner(text, color):
	draw_text = WINNER_FONT.render(text, 1, color)
	WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
	pygame.display.update()
	pygame.time.delay(5000)

def main():
	# left
	red = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
	# right
	yellow = pygame.Rect(1820, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

	current_round = 1
	frames_since_last = 0
	round_length = 1800
	max_bullets = 2 + current_round
	VELOCITY = 10
	BULLET_VELOCITY = VELOCITY * 1.4

	red_bullets = []
	yellow_bullets = []
	red_health = 5
	yellow_health = 5

	clock = pygame.time.Clock()
	

	run = True
	
	while(run):
		
		clock.tick(FPS)
		frames_since_last += 1
		if frames_since_last >= round_length:
			current_round += 1
			frames_since_last = 0
			round_length = 1800 * math.fabs(math.log10(1 / current_round) + 1)
			VELOCITY = 10 * (math.log10(current_round) + 1)
			red_health += 1
			yellow_health += 1

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_LCTRL and len(red_bullets) < max_bullets:
					bullet = pygame.Rect(red.x + red.width, red.y + red.height // 2, 20, 10)
					red_bullets.append(bullet)

				if event.key == pygame.K_RCTRL and len(yellow_bullets) < max_bullets:
					bullet = pygame.Rect(yellow.x, yellow.y + yellow.height // 2, 20, 10)
					yellow_bullets.append(bullet)

			if event.type == RED_HIT:
				red_health -= 1
			if event.type == YELLOW_HIT:
				yellow_health -= 1
		
		
		winner_text = ""
		color = ()
		if red_health <= 0:
			winner_text = "Yellow Wins"
			color = (255, 255, 0)

		if yellow_health <= 0:
			winner_text = "Red Wins"
			color = (255, 0, 0)
		
		if winner_text != "":
			draw_winner(winner_text, color)
			break

		keys_pressed = pygame.key.get_pressed()
		handle_input(red, keys_pressed, False, VELOCITY)
		handle_input(yellow, keys_pressed, True, VELOCITY)

		handle_bullets(yellow_bullets, red_bullets, yellow, red, BULLET_VELOCITY)

		draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, current_round, round_length, frames_since_last)

	main()

if __name__ == "__main__":
	main()