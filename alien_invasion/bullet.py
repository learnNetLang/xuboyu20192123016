#*coding:utf-8*
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	#����ɴ��������ӵ�����
	def __init__(self,ai_game):
		#�ڷɴ���ǰλ�ô���һ���ӵ�����
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color
		
		#��(0,0)������һ����ʾ�ӵ��ľ��Σ���������ȷ��λ��
		self.rect = pygame.Rect(0,0,self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop
		
		#�洢��С����ʾ���ӵ�λ��
		self.y = float(self.rect.y)
	def update(self):
		#�����ƶ��ӵ�
		#���±�ʾ�ӵ�λ�õ�С��ֵ
		self.y -= self.settings.bullet_speed
		#���±�ʾ�ӵ���rect��λ��
		self.rect.y = self.y
	
	def draw_bullet(self):
		#����Ļ�ϻ����ӵ�
		pygame.draw.rect(self.screen,self.color,self.rect)
