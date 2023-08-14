import pygame
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

	def collision(self, axis):
		for sprite in self.world.getArr():
			if sprite.rect.colliderect(self.rect):
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

	def move(self, dt):
		# horizontal movement
		if(self.isMoving[0] == True):
			if self.movement_sound_timer > 0:
				self.movement_sound_timer -= 1

			if self.movement_sound_timer == 0 and self.on_floor == True:
				self.movement_sound_timer = SOUND_PLAYING_DELAY
				self.publisher.notify(EventsEnum.movement.value)
	
			self.dx = self.speed
			self.rect.x += self.direction.x * self.dx * dt
			self.collision('x')

		# vertical movement
		if(self.isMoving[1] == True):
			if(self.on_floor == True):
				self.dy = self.jump_speed
				if self.jumpCounter < self.baseJumpSpeed:
					self.rect.y += self.dy * dt
					self.jumpCounter += 1
					self.collision('y')
				else:
					self.on_floor = False	
				
				
	def update(self, dt):
		if(currentLevel == LevelEnum.Platformer.value):
			self.dy = self.gravity
			self.rect.y += self.dy * dt

			self.collision('y')
			self.move(dt)
					
		if(currentLevel == LevelEnum.Strategy.value):
			# if(self.isMoving[1] == True):
			# 	self.rect.y += self.direction.y * self.speed * dt
			pass

	def draw(self):
		self.display_surface.blit(self.image, self.rect.topleft)