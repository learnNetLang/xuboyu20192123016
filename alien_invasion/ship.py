#*coding:utf-8*
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	#����ɴ�����
	
	def __init__(self,ai_game):
		#��ʼ���ɴ����������ʼλ��
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()
		
		#���طɴ�ͼ�񲢻�ȡ����Ӿ���
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		
		#����ÿ���·ɴ�,�����������Ļ�ײ�������
		self.rect.midbottom = self.screen_rect.midbottom
		
		#�ڷɴ�������x�д洢С��ֵ
		self.x = float(self.rect.x)
		
		#�ƶ���־
		self.moving_right = False
		self.moving_left = False
	
	def update(self):
		#�����ƶ���־�����ɴ���λ��
		#���·ɴ�������rect�����xֵ
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed
		
		#����self.x����rect����
		self.rect.x = self.x
	
	def blitme(self):
		#��ָ��λ�û��Ʒɴ�
		self.screen.blit(self.image,self.rect)
	
	def center_ship(self):
		#�÷ɴ�����Ļ�׶˾���
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
