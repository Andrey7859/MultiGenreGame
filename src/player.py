import pygame
import config
from config import *

class Player(pygame.sprite.Sprite):
	def __init__(self, world, publisher):
		# super().__init__(groups)
		self.display_surface = pygame.display.get_surface()
		self.world = world
		self.publisher = publisher
		self.image = pygame.Surface((TILE_SIZE // 2,TILE_SIZE))
		self.image.fill('green')
		self.rect = self.image.get_rect(center = (WIDTH / 2, 0))
		self.coord_offset = pygame.math.Vector2()

		self.health = 100
		self.damage = 34

		# player movement 
		self.direction = pygame.math.Vector2()
		self.dx = 0
		self.dy = 0
		self.speed = 12
		self.gravity = 9.8
		self.jump_speed = -TILE_SIZE
		self.baseJumpSpeed = 16
		self.on_floor = False
		self.jumpCounter = 1
		self.isMoving = [False, False]
		self.movement_sound_timer = 0

	def horizontalMovement(self, direction, isMoving):
		self.isMoving[0] = isMoving
		self.direction.x = direction

	def verticalMovement(self, direction, isMoving):
		self.isMoving[1] = isMoving

		if(currentLevel == LevelEnum.Platformer.value):
			if(self.on_floor == True):
				self.publisher.notify(EventsEnum.jump.value)
			
		if(currentLevel == LevelEnum.Strategy.value):
			self.direction.y = direction

	def setPos(self, x, y):
		self.coord_offset.x = x
		self.coord_offset.y = y

	def collision(self, axis, enemies):
		for sprite in self.world.getArr():
			if sprite.rect.colliderect(self.rect):
				if(sprite.objType == TileEnum._None.value):

					#Horizont
					if axis == 'x':
						if self.direction.x > 0: 
							self.rect.right = sprite.rect.left

						if self.direction.x < 0: 
							self.rect.left = sprite.rect.right

					#Vertical
					if axis == 'y':
						if self.dy > 0:
							self.rect.bottom = sprite.rect.top
							self.dy = 0
							self.on_floor = True
							self.jumpCounter = 1

						if self.dy < 0:
							self.rect.top = sprite.rect.bottom
							self.dy = 0
				
				if(sprite.objType == TileEnum.Coin.value):
					self.world.getArr().remove(sprite)
					tmp = int(savedValues["total_score"]) + 1
					savedValues['total_score'] = str(tmp)
					self.publisher.notify(EventsEnum.collectCoin.value)

				if(sprite.objType == TileEnum.Portal.value):
					print('touch portal')

		for enemy in enemies.getAllEnemies():
			if enemy.rect.colliderect(self.rect):
				if(enemy.objType == TileEnum.Enemies.value):
					if axis == 'y':
						if self.dy > 0:
							self.rect.bottom = enemy.rect.top
							self.dy = 0
							enemies.getAllEnemies().remove(enemy)

					if axis == 'x':
						if self.direction.x > 0: 
							self.rect.right = enemy.rect.left
							self.health = self.health - 20
							print("health", self.health)
							print(self.rect)
							self.rect.x = self.rect.x - 50

						if self.direction.x < 0: 
							self.rect.left = enemy.rect.right
							self.health = self.health - 20
							print("health", self.health)
							self.rect.x = self.rect.x + 50

	def move(self, dt, enemies):
		# horizontal movement
		if(self.isMoving[0] == True):
			if self.movement_sound_timer > 0:
				self.movement_sound_timer -= 1

			if self.movement_sound_timer == 0 and self.on_floor == True:
				self.movement_sound_timer = SOUND_PLAYING_DELAY
				self.publisher.notify(EventsEnum.movement.value)
	
			self.dx = self.speed
			self.rect.x += self.direction.x * self.dx * dt
			self.collision('x', enemies)

		# vertical movement
		if(self.isMoving[1] == True):
			if(self.on_floor == True):
				self.dy = self.jump_speed
				if self.jumpCounter < self.baseJumpSpeed:
					self.rect.y += self.dy * dt
					self.jumpCounter += 1
					self.collision('y', enemies)
				else:
					self.on_floor = False	
				
	def checkHorizont(self):
		if(self.rect.y > 600):
			config.gameState = UIEnum.GameOver.value
				
	def update(self, dt, enemies):
		if(currentLevel == LevelEnum.Platformer.value):
			self.dy = self.gravity
			self.rect.y += self.dy * dt

			self.collision('y', enemies)
			self.move(dt, enemies)
			self.checkHorizont()
					
		if(currentLevel == LevelEnum.Strategy.value):
			# if(self.isMoving[1] == True):
			# 	self.rect.y += self.direction.y * self.speed * dt
			pass

	def draw(self):
		self.display_surface.blit(self.image, self.rect.topleft)