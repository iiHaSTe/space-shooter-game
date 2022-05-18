from pygame import *



class Sprite(sprite.Sprite):
	def __init__(self, path, position, size=None, prop={}, speed=[5, 5]):
		super().__init__()
		
		self.path = path
		self.image = image.load(self.path)
		self.rect = self.image.get_rect()
		self.speed = speed
		self.prop = prop
		self.clones = []
		self.deg = 0
		if not size is None:
			self.rect.size = size
			self.image = transform.scale(self.image, (int(size[0]), int(size[1])))
		self.rect.x = position[0]
		self.rect.y = position[1]
	
	def set_x(self, x):
		self.rect.x = x
	def get_x(self):
		return self.rect.x
	def set_y(self, y):
		self.rect.y = y
	def get_y(self):
		return self.rect.y
	def add_x(self, x):
		self.rect.x += x
	def add_y(self, y):
		self.rect.y += y
	def set_pos(self, pos):
		self.set_x(pos[0])
		self.set_y(pos[1])
	def get_pos(self):
		return (self.get_x(), self.get_y())
	def move(self, speed=None):
		if speed is None:
			self.add_x(self.speed[0])
			self.add_y(self.speed[1])
		else:
			self.add_x(speed[0])
			self.add_y(speed[1])
	
	def rotate(self, deg):
		self.image = transform.rotate(self.image, deg)
		self.deg = deg
	def copy(self):
		return Sprite(
			self.path,
			(self.rect.x, self.rect.y),
			self.rect.size,
			self.prop,
			self.speed
		)
	
	def clicked(self):
		return mouse.get_pressed()[0] and self.rect.collidepoint(mouse.get_pos())
	
	def colliderect(self, costomSprite):
		try:
			return self.rect.colliderect(costomSprite.rect)
		except:
			n = False
			for i in costomSprite:
				if self.rect.colliderect(i.rect):
					return True
					break
			return n
