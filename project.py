import pygame
from sys import exit
import random

pygame.init()

#class Player, class enemy, def collision mech, score

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.p1 = pygame.image.load('Player/R1.png').convert_alpha()
		self.p2 = pygame.image.load('Player/R2.png').convert_alpha()
		self.p3 = pygame.image.load('Player/R3.png').convert_alpha()
		self.p4 = pygame.image.load('Player/R4.png').convert_alpha()
		self.p5 = pygame.image.load('Player/R5.png').convert_alpha()
		self.p6 = pygame.image.load('Player/R6.png').convert_alpha()
		self.p7 = pygame.image.load('Player/R7.png').convert_alpha()
		self.p8 = pygame.image.load('Player/R8.png').convert_alpha()
		self.p9 = pygame.image.load('Player/R9.png').convert_alpha()
		self.pw, self.ph = self.p1.get_size()

		self.p_frames = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8, self.p9]
		self.p_index = 0
		self.image = self.p_frames[self.p_index]
		self.rect = self.image.get_rect(midbottom=(100,400))

		self.g = 0

	def p_ani(self):
		self.p_index += 0.3
		if self.p_index > len(self.p_frames)-1:
			self.p_index = 0
		self.image = self.p_frames[int(self.p_index)]

		keys = pygame.key.get_pressed()
		if (keys[pygame.K_SPACE] or keys[pygame.K_UP])and self.rect.y == 350:
			self.g = -15

		if keys[pygame.K_DOWN]:
			self.image = pygame.transform.scale(self.p_frames[int(self.p_index)], ((self.pw*3)//4, (self.ph*3)//4))
			self.rect = self.image.get_rect(midbottom=(100, 415))

	def gravity(self):
		keys = pygame.key.get_pressed()
		if not keys[pygame.K_DOWN]:
			self.g += 1
			self.rect.y += self.g
			if self.rect.y >= 350:
				self.rect.y = 350
				self.g = 0

	def update(self):
		self.p_ani()
		self.gravity()


class Enemies(pygame.sprite.Sprite):
	def __init__(self, choice):
		super().__init__()
		s1_ = pygame.image.load('snail/snail1.png').convert_alpha()
		s1w, s1h = s1_.get_size()
		s1 = pygame.transform.scale(s1_, ((s1w*3)//4, (s1h*3)//4))

		s2_ = pygame.image.load('snail/snail2.png').convert_alpha()
		s2w, s2h = s2_.get_size()
		s2 = pygame.transform.scale(s2_, ((s2w*3)//4, (s2h*3)//4))

		f1_ = pygame.image.load('Fly/Fly1.png').convert_alpha()
		f1w, f1h = f1_.get_size()
		f1 = pygame.transform.scale(f1_, ((f1w*3)//4, (f1h*3)//4))

		f2_ = pygame.image.load('Fly/Fly2.png').convert_alpha()
		f2w, f2h = f2_.get_size()
		f2 = pygame.transform.scale(f2_, ((f2w*3)//4, (f2h*3)//4))

		self.choice = choice

		if self.choice == 'snail':
			self.frames = [s1, s2]
			self.index = 0
			self.image = self.frames[self.index]
			self.rect = self.image.get_rect(midbottom=(900,410))
		else:
			self.frames = [f1, f2]
			self.index = 0
			self.image = self.frames[self.index]
			self.rect = self.image.get_rect(midbottom=(900,360))

	def e_ani(self):
		if self.choice == 'snail':
			self.rect.x -= 5
			self.index += 0.3
			if self.index > len(self.frames)-1:
				self.index = 0
			self.image = self.frames[int(self.index)]
		else:
			self.rect.x -= 5
			self.index += 0.4
			if self.index > len(self.frames)-1:
				self.index = 0
			self.image = self.frames[int(self.index)]

	def destroy(self):
		if self.rect.x <= -100:
			self.kill()

	def update(self):
		self.e_ani()
		self.destroy()


clock = pygame.time.Clock()

screen = pygame.display.set_mode((800,480))
bg = pygame.image.load('bg.jpg').convert_alpha()

font = pygame.font.Font('font/Pixeltype.ttf', 40)

start_button = font.render('Start', False, 'Black')
start_button_rect = start_button.get_rect(center=(400,50))

restart_button = font.render('Restart', False, 'Black')
restart_button_rect = restart_button.get_rect(center=(400,50))

score_text = font.render('Score: ', False, 'Black')
score_text_rect = score_text.get_rect(center=(390, 90))

h_score_text = font.render('Highest score: ', False, 'Black')
h_score_text_rect = h_score_text.get_rect(center=(640, 90))

player = pygame.sprite.GroupSingle()   #GroupSingle
player.add(Player())

enemies = pygame.sprite.Group()

def collision():
	x = pygame.sprite.spritecollide(player.sprite, enemies, False)
	if x:
		return False
	else:
		return True

def score(fs:int):
	score = int(pygame.time.get_ticks()/100) - fs
	dis_score = font.render(f"{score}", False, 'Black')
	dis_score_rect = dis_score.get_rect(center=(455, 90))
	screen.blit(dis_score, dis_score_rect)
	return score



#creating new event for spawning of enemies
e_timer = pygame.USEREVENT + 1
pygame.time.set_timer(e_timer, 1000)


def main():
	hs = 0
	temp = open("scores.txt", "w")
	temp.write("0")  #ensures that the game will work even if the scores file is empty initially
	temp.close()
	start_screen = True
	game_start = False
	restart = False

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				f = open("scores.txt", "w")  #resets scores highest val to 0 once the game is closed
				f.write("0")
				pygame.quit()
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN and start_button_rect.collidepoint(event.pos):
				start_screen = False
				game_start = True
				restart = False

			if game_start and event.type == e_timer:
				enemies.add(Enemies(random.choice(['snail', 'snail', 'snail', 'fly'])))

			if not game_start:
				restart = True
				f1 = open("scores.txt", "r")
				hs = int(f1.read())

			if event.type == pygame.MOUSEBUTTONDOWN and restart_button_rect.collidepoint(event.pos):
				filler_score = int(pygame.time.get_ticks()/100)
				game_start = True
				start_screen = False
				restart = False
				enemies.empty()


		screen.blit(bg, (0,0))  # for the bg

		if start_screen:
			screen.blit(start_button, start_button_rect)

		elif game_start:
			screen.blit(score_text, score_text_rect)
			enemies.draw(screen)
			enemies.update()

			game_start = collision()  #goes to restart window
			s = score(filler_score)

			screen.blit(h_score_text, h_score_text_rect)

			hs_text = font.render(f"{hs}", False, 'Black')
			hs_text_rect = hs_text.get_rect(center=(760, 90))
			screen.blit(hs_text, hs_text_rect)

		elif restart:
			enemies.draw(screen)
			player.draw(screen)
			screen.blit(restart_button, restart_button_rect)
			screen.blit(score_text, score_text_rect)

			final_score = font.render(f"{s}", False, 'Black')
			final_score_rect = final_score.get_rect(center=(455,90))
			screen.blit(final_score, final_score_rect)

			scores_file_r = open("scores.txt", "r")
			try:   #the file by default has score 0
				if int(scores_file_r.read()) < s:
					scores_file_w = open("scores.txt", "w")
					scores_file_w.write(str(s))
			except ValueError:
				pass

			scores_file_w.close()
			scores_file_r.close()


		if game_start or start_screen:
			player.draw(screen)
			player.update()

		pygame.display.update()
		clock.tick(60)

if __name__ == "__main__":
  main()