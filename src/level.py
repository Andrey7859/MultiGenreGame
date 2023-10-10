import pygame
import config
from config import *
from player import *

M90 = 1610612736
P90 = 2684354560
P180 = M90 * 2

ID_OFFSET = 986

class Layer:
	def __init__(self, path):
		self.path = path

		self.map = []
		self.numbers = set()
		self.tilesDict = {}

	def __translitID(self, id):
		if(len(id) > 4):
			m90_local = str(int(id) - M90 - 1)
			p180_local = str(int(id) - P180 - 1)
			p90_local = str(int(id) - P90 - 1)

			if(len(m90_local) > 0 and len(m90_local) < 4):
				return [m90_local, 90]
			
			if(len(p180_local) > 0 and len(p180_local) < 4):
				return [p180_local, 180]
		
			if(len(p90_local) > 0 and len(p90_local) < 4):
				return [p90_local, -90]
			
			return ['', 0]

		else:
			return [id, 0]

	def loadlayer(self, desirable_layer= 0):
		if (currentLevel == LevelEnum.Strategy.value):
			self.loadStrategylayer(desirable_layer)
		
		if (currentLevel == LevelEnum.Shooter.value or currentLevel == LevelEnum.Platformer.value):
			self.loadOtherLayer()

	def loadStrategylayer(self, desirable_layer):
		with open(self.path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break

				if line.find('<layer ') != -1:
					layer = int(line.split(' ')[1].split('"')[1])
					
					if(layer == desirable_layer):
						line = f.readline()

						while True:
							line = f.readline()

							if line.find('</data>') != -1:
								break

							line = line.replace('\n', '').split(',')
							tmp = []

							for i in range(len(line)):
								matrix = []

								mod_line = self.__translitID(line[i])
								line[i] = mod_line[0]
								rotation = mod_line[1]
								
								if (len(line[i]) > 0):
									self.numbers.add(line[i])

								if(layer == 1):
									matrix.append(line[i])

								if(layer == 3 or layer == 4):
									if(line[i] in self.tilesDict.keys()):
										matrix.append(line[i])
									else:
										matrix.append('0')
								
								matrix.append(rotation)
								tmp.append(matrix)

							self.map.append(tmp)
						break

			# for i in level_layer:
			# 	CriticalLogger.critical(i)

			# InfoLogger.info(' ')

	def loadOtherLayer(self):
		with open(self.path, "r") as f:
			while True:
				line = f.readline()

				if not line:
					break
				
				line = line.replace('\n', '').split(',')
				self.map.append(line)
				
				# for i in line:
				# 	self.terrainLayer[0].numbers.add(i)

class Parser:
	def __init__(self, terrain, assetMngr):
		self.terrainLayer = terrain		# ЭТО МАССИВ
		self.assetMngr = assetMngr

	def __getTerrainIDs(self, path):
		with open(path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break
		
				if line.find('<tileset ') != -1:
					if (line.find('firstgid=') != -1):
						id = line[line.find('firstgid=') : line.find(' name=')].split('"')[1]
						
						if(id == "1"):
							while True:
								line = f.readline()
								line = f.readline()

								if line.find("</tileset>") != -1:
									break

								id = str(int(line[line.find('"') + 1 : line.rfind('"')]))	# get ID

								line = f.readline()									# get path of the image
								line = line[line.find('media') : len(line)]
								line = line.replace('"/>\n', '')
								line = line.split('/')[-1].split('.')[0]

								image = self.assetMngr.getImage(line)
								self.terrainLayer[0].tilesDict[id] = image							# create dict

							break

		# for i in self.terrainLayer.tilesDict:
			# InfoLogger.info(i + " " + self.terrainLayer.tilesDict[i])
		
	def __getCastlesIDs(self, path):
		with open(path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break

				if line.find('<tileset ') != -1:
					if (line.find('firstgid=') != -1):
						id = line[line.find('firstgid=') : line.find(' name=')].split('"')[1]
						
						if(id != 1):
							self.terrainLayer[1].numbers.add(id)

							line = f.readline()
							if(line.find('<image ') != -1):
								line = line[line.find('source=') : line.find('width=')].split('"')[1]
								line = line.split('/')[-1].split('.')[0]

								image = self.assetMngr.getImage(line)
								self.terrainLayer[1].tilesDict[id] = image
		
		# for i in self.terrainLayer[1].tilesDict:
		# 	InfoLogger.info(i + " " + self.terrainLayer[1].tilesDict[i])

	def __getLandscapeIDs(self, path):
		with open(path, 'r') as f:
			while True:
				line = f.readline()

				if not line:
					break
		
				if line.find('<tileset ') != -1:
					if line.find('name="Landscape"') != -1:
						while True:
							line = f.readline()
							line = f.readline()

							if line.find("</tileset>") != -1:
								break

							id = str(int(line[line.find('"') + 1 : line.rfind('"')]) + ID_OFFSET)	# get ID

							line = f.readline()									# get path of the image
							line = line[line.find('..') : len(line)]
							line = line.replace('"/>\n', '')
							line = line.split('/')[-1].split('.')[0]
							
							image = self.assetMngr.getImage(line)
							self.terrainLayer[2].tilesDict[id] = image
						break

		# for i in self.terrainLayer[2].tilesDict:
		# 	InfoLogger.info(i + " " + self.terrainLayer[2].tilesDict[i])

	def __getTilesFromTileset(self, layer, path, size, id, scale_factor= 1):
		tileset = pygame.image.load(path).convert()
		tileset = pygame.transform.scale(tileset, (tileset.get_width() / scale_factor, tileset.get_height() / scale_factor))

		# id = 1

		for y in range(size[1]):			# size[1] - height
			for x in range(size[0]):		# size[0] - width
				layer.tilesDict[str(id)] = tileset.subsurface([x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE])
				id += 1

		# for i in self.terrainLayer[0].tilesDict:
		# 	InfoLogger.info(str(i) + " " + str(self.terrainLayer[0].tilesDict[i]))

	def mainParcer(self, path):
		if path[0].split('.')[1] == 'txt':
			InfoLogger.info("Loading .txt map")
			self.parceTXT(path)
		else:
			InfoLogger.info("Loading .tmx map")
			self.parceTMX(path[0])

	def parceTXT(self, path):
		# creating [id] = [image] dictionary
		if (currentLevel == LevelEnum.Shooter.value):
			self.__getTilesFromTileset(0, path[1], (6, 18), 2)

		if (currentLevel == LevelEnum.Platformer.value):
			self.__getTilesFromTileset(self.terrainLayer[0], path[2], (8, 16), 1)
			self.__getTilesFromTileset(self.terrainLayer[1], path[3], (1, 1), 128)
			self.__getTilesFromTileset(self.terrainLayer[2], path[5], (1, 1), 777777)
			self.__getTilesFromTileset(self.terrainLayer[3], path[7], (1, 1), 888888)
		# creating map from the file
		self.terrainLayer[0].loadlayer()
		self.terrainLayer[1].loadlayer()
		self.terrainLayer[2].loadlayer()
		self.terrainLayer[3].loadlayer()

	def parceTMX(self, path):
		# creating [id] = [image's path] dictionary
		self.__getTerrainIDs(path)
		self.__getCastlesIDs(path)
		self.__getLandscapeIDs(path)

		# creating map from the file
		self.terrainLayer[0].loadlayer(1)
		self.terrainLayer[1].loadlayer(3)
		self.terrainLayer[2].loadlayer(4)

class Tile:
	def __init__(self, assetMngr, pos, objType, image, rotation = 0, scale = 1):
		self.id = 0
		self.display_surface = pygame.display.get_surface()
		self.assetMngr = assetMngr
		self.isVisible = True
		self.objType = objType
		self.pos = pos

		# self.image = self.assetMngr.getImage(img_path)
		self.image = image
		self.image = pygame.transform.rotate(self.image, rotation)
		self.image = pygame.transform.scale(self.image, (self.image.get_width() / scale, self.image.get_height() / scale))
		self.rect = self.image.get_rect(center = pos)

	def setVisible(self, visible):
		self.isVisible = visible

	def draw(self):
		if(self.isVisible == True):
			self.display_surface.blit(self.image, self.rect.topleft)

class TilesObjectPool:
	def __init__(self):
		self.arr = []

	def append(self, obj):
		obj.id = len(self.arr)
		self.arr.append(obj)

	def getArr(self):
		return self.arr

	def draw(self):
		for obj in self.arr:
			obj.draw()

class Level:
	def __init__(self, assetMngr, publisher, isMiniMap= False):
		self.display_surface = pygame.display.get_surface()
		self.assetMngr = assetMngr
		self.isMiniMap = isMiniMap

		self.scale = 16
		self.tiles = TilesObjectPool()
		# self.camera = Camera(self.tiles, publisher)
		# self.camera = CameraGroup(self.tiles, publisher)

	def setup_level(self, player, path):
		self.player = player

		if (config.currentLevel == LevelEnum.Strategy.value):
			self.terrainLayer = [Layer(path[0]), Layer(path[0]), Layer(path[0])]

			self.parser = Parser(self.terrainLayer, self.assetMngr)
			self.parser.mainParcer(path)
				
			if (self.isMiniMap == True):
				self.strategyLoader(self.terrainLayer[0], self.scale)
				self.strategyLoader(self.terrainLayer[1], self.scale)
				self.strategyLoader(self.terrainLayer[2], self.scale)
			else:
				self.strategyLoader(self.terrainLayer[0])
				self.strategyLoader(self.terrainLayer[1])
				self.strategyLoader(self.terrainLayer[2])

		if (config.currentLevel == LevelEnum.Shooter.value):
			self.terrainLayer = [Layer(path[0])]
			
			self.parser = Parser(self.terrainLayer, self.assetMngr)
			self.parser.mainParcer(path)

			self.shooterLoader(self.terrainLayer[0])

		if (config.currentLevel == LevelEnum.Platformer.value):
			self.terrainLayer = [Layer(path[0]), Layer(path[1]), Layer(path[4]), Layer(path[6])]
			
			self.parser = Parser(self.terrainLayer, self.assetMngr)
			self.parser.mainParcer(path)

			self.platformerLoader(self.terrainLayer[0])
			self.platformerLoader(self.terrainLayer[1])
			self.platformerLoader(self.terrainLayer[2])
			self.platformerLoader(self.terrainLayer[3])

	def strategyLoader(self, layer, scale= 1):
		for row_index, row in enumerate(layer.map):
			for col_index, col in enumerate(row):
				if(self.isMiniMap == True):
					x = ((col_index * TILE_SIZE) / scale) + WIDTH - (len(layer.map) * 2)
					y = (row_index * TILE_SIZE) / scale
				
				else:
					x = (col_index * TILE_SIZE) / scale
					y = (row_index * TILE_SIZE) / scale

				if col[0] in layer.numbers and col[0] != '0':
					self.tiles.append(Tile(self.assetMngr, (x, y), TileEnum._None.value, layer.tilesDict[col[0]], col[1], scale))
				
				if col[0] == '18324':
					self.player.setPos(x, y)

	def shooterLoader(self, layer):
		# for row_index,row in enumerate(self.matrix):
		for row_index, row in enumerate(layer.map):
			for col_index, col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE
				for currWall in layer.tilesDict.keys():
					if col == str(currWall):
						self.tiles.append(Tile(self.assetMngr, (x,y), TileEnum._None.value, layer.tilesDict.get(col), 0))
					if col == '18324':
						self.player.setPos(x, y)
					
	def platformerLoader(self, layer):
		for row_index, row in enumerate(layer.map):
			for col_index, col in enumerate(row):
				x = col_index * TILE_SIZE
				y = row_index * TILE_SIZE

				if (col in layer.tilesDict.keys()) and col == '777777':
					self.tiles.append(Tile(self.assetMngr, (x,y), TileEnum.Portal.value, layer.tilesDict.get(col)))
				
				if (col in layer.tilesDict.keys()) and col == '888888':
					self.tiles.append(Tile(self.assetMngr, (x,y), TileEnum.Buff.value, layer.tilesDict.get(col)))

				if (col in layer.tilesDict.keys()) and col == '128':
					self.tiles.append(Tile(self.assetMngr, (x,y), TileEnum.Coin.value, layer.tilesDict.get(col)))
					InfoLogger.info("Coin at the position: " + str(x) + ' ' + str(y))
				
				if (col in layer.tilesDict.keys()) and col != '128' and col != '777777' and col != '888888':
					self.tiles.append(Tile(self.assetMngr, (x,y), TileEnum._None.value, layer.tilesDict.get(col)))
									

	def getGroups(self):
		return [self.visible_sprites, self.active_sprites]

	def getCollSprites(self):
		return self.collision_sprites

	def draw(self, offset):
		# self.camera.followPlayer(dt, self.player, self.scale, self.isMiniMap)	# Draw the map
		# self.camera.custom_draw(self.player)
		# self.player.draw()

		for sprite in self.tiles.getArr():
			offset_pos = round(sprite.rect.topleft - offset)
			self.display_surface.blit(sprite.image, offset_pos)

		# pass
