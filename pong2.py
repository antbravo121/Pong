import pygame
import random
pygame.init()


class Paddle:
	def __init__(self, x, y, width, height, player_id):
		self.x = x
		self.y = y
		#paddle num is which player this paddle belongs to, ex: paddle A: 1 or paddle B: 2
		self.player_id = player_id
		self.width = width
		self.height = height
		self.speed = 4
		self.rect = (x, y, width, height)
		self.color = (255,255,255)

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)

	def move(self):
		keys = pygame.key.get_pressed()
		#Update y values
		if self.player_id == 1:
			if keys[pygame.K_w]:
				self.y -= self.speed
			if keys[pygame.K_s]:
				self.y += self.speed

		if self.player_id == 2:
			if keys[pygame.K_UP]:
				self.y -= self.speed
			if keys[pygame.K_DOWN]:
				self.y += self.speed

		#Check boundaries
		self.check_boundaries()

		#Update values
		self.rect = (self.x, self.y, self.width, self.height)

	def check_boundaries(self):
		if self.y <= 0:
			self.y = 0
		elif self.y >= 400:
			self.y = 400


class Ball(Paddle):
	def __init__(self, x, y, width, height, player_id):
		super().__init__(x, y, width, height, player_id)
		self.speed_x = random.choice([-3,3])
		self.speed_y = random.choice([-3,3])
		self.origin = (x, y)
		self.score_A = 0
		self.score_B = 0

	def move(self):
		self.x += self.speed_x
		self.y += self.speed_y
		#Check Left/Right boundaries
		self.check_boundaries()

		#Update values
		self.rect = (self.x, self.y, self.width, self.height)

	def check_boundaries(self):
		# Top/Bottom Boundaries
		if self.y <= 0:
			self.y = 0
			self.speed_y *= -1
		if self.y >= 590:
			self.y = 590
			self.speed_y *= -1

		# Left/Right Boundaries
		if self.x <= 0:
			self.reset_n_score("B")
		if self.x >= 790:
			self.reset_n_score("A")

	def reset_n_score(self, player):
		# Add a point to player and reset the position of ball and change speed
		if player == "B":
			self.score_B += 1
		elif player == "A":
			self.score_A += 1

		self.x = self.origin[0]
		self.y = self.origin[1]
		self.speed_x = random.choice([-3,3])
		self.speed_y = random.choice([-3,3])
	
	def check_paddle_collision(self, paddle):
		# Create rect objects to use pygame's built in collision dectector
		temp_rect = pygame.Rect(self.x, self.y, self.width, self.height)
		paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.width, paddle.height)
		return temp_rect.colliderect(paddle_rect)


def draw_score(screen, score, x, y):
	font = pygame.font.Font("freesansbold.ttf", 35)
	score = font.render(str(score), True, (255,255,255))
	screen.blit(score, (x, y))

def redraw_window(screen, paddle_A, paddle_B, ball):
	# Draw all elements on screen
	screen.fill((0,0,0))
	paddle_A.draw(screen)
	paddle_B.draw(screen)
	ball.draw(screen)
	draw_score(screen, ball.score_A, 355, 10)
	draw_score(screen, ball.score_B, 410, 10)
	pygame.display.update()


def main():
	screen = pygame.display.set_mode((800, 600))

	font = pygame.font.Font("freesansbold.ttf", 35)

	# Create paddles and ball
	paddle_A = Paddle(5, 200, 10, 200, 1)
	paddle_B = Paddle(785, 200, 10, 200, 2)
	ball = Ball(375, 275, 10, 10, 1)

	running = True
	while running:
		# Check if player quit
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# Move paddles and ball
		paddle_A.move()
		paddle_B.move()
		ball.move()

		# Check Paddle Collision
		if ball.check_paddle_collision(paddle_A):
			ball.x = paddle_A.x + ball.width
			ball.speed_x *= -1
		elif ball.check_paddle_collision(paddle_B):
			ball.x = paddle_B.x - ball.width
			ball.speed_x *= -1

		redraw_window(screen, paddle_A, paddle_B, ball)

main()
