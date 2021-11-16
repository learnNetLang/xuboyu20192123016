#*coding:utf-8*
import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	#������Ϸ��Դ����Ϊ����
	def __init__(self):
		#��ʼ����Ϸ��������Ϸ��Դ
		pygame.init()
		self.settings = Settings()
		
		self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")
		
		#�����洢��Ϸͳ����Ϣ��ʵ��
		#�������Ƿ���
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)
		
		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()
		
		self._create_fleet()
		
		#����Play��ť
		self.play_button = Button(self,"Play")
	
	def _create_fleet(self):
		#����������Ⱥ
		#����һ�������˲�����һ�п����ɶ��ٸ�������
		#�����˵ļ��Ϊ�����˿��
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2*alien_width)
		number_aliens_x = available_space_x // (2*alien_width)
		
		#������Ļ�����ɶ�����������
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
								(3*alien_height) - ship_height)
		number_rows = available_space_y // (2*alien_height)
		
		#����������Ⱥ
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)
	
	def _check_fleet_edges(self):
		#�������˵����Եʱ��ȡ��Ӧ�Ĵ�ʩ
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_dircation()
				break
	
	def _change_fleet_dircation(self):
		#����Ⱥ���������ƣ����ı����ǵķ���
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1
	
	def _create_alien(self,alien_number,row_number):
		#����һ�������˲�������뵱ǰ��
		alien = Alien(self)
		alien_width,alien_height = alien.rect.size
		alien.x = alien_width + 2*alien_width*alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
		self.aliens.add(alien)
		

	def run_game(self):
		#��ʼ��Ϸ����ѭ��
		while True:
			self._check_events()
			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()
			
			self._update_screen()
	
	def _update_aliens(self):
		#����Ƿ���������λ����Ļ��Ե
		#����������Ⱥ�����������˵�λ��
		self._check_fleet_edges()
		self.aliens.update()
		
		#��������˺ͷɴ�֮�����ײ
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			self._ship_hit()
		
		#����Ƿ��������˵�������Ļ�׶�
		self._check_aliens_bottom()
	
	def _ship_hit(self):
		#��Ӧ�ɴ���������ײ��
		if self.stats.ships_left > 0:
			#��ships_left��1�����¼Ƿ���
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			
			#������µ������˺��ӵ�
			self.aliens.empty()
			self.ship.center_ship()
			
			#��ͣ
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)
	
	def _update_bullets(self):
		#�����ӵ���λ�ò�ɾ����ʧ���ӵ�
		#�����ӵ���λ��
		self.bullets.update()
			
		#ɾ����ʧ���ӵ�
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)
		
		self._check_bullet_alien_collisions()
	
	def _check_bullet_alien_collisions(self):	
		#��Ӧ�ӵ�����������ײ
		#ɾ��������ײ���ӵ���������
		collisions = pygame.sprite.groupcollide(
				self.bullets,self.aliens,True,True)
		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()
		if not self.aliens:
			#ɾ�����е��ӵ����½�һȺ������
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()
			
			#��ߵȼ�
			self.stats.level += 1
			self.sb.prep_level()
	
	def _check_aliens_bottom(self):
		#����Ƿ��������˵�������Ļ�׶�
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#��ɴ���ײ��һ������
				self._ship_hit()
				break
			
	def _check_events(self):
		#��Ӧ���̺�����¼�
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)
	
	def _check_play_button(self,mouse_pos):
		#����ҵ���Play��ťʱ��ʼ����Ϸ
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#������Ϸ����
			self.settings.initialize_dynamic_settings()
			
			#������Ϸͳ����Ϣ
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()
			
			#������µ������˺��ӵ�
			self.aliens.empty()
			self.bullets.empty()
			
			#����һȺ�����˲��÷ɴ�����
			self._create_fleet()
			self.ship.center_ship()
			
			#���������
			pygame.mouse.set_visible(False)
	
	def _check_keydown_events(self,event):
		#��Ӧ����
			if event.key == pygame.K_RIGHT:
			#�����ƶ��ɴ�
				self.ship.moving_right = True
			elif event.key == pygame.K_LEFT:
			#�����ƶ��ɴ�
				self.ship.moving_left = True
			elif event.key == pygame.K_q:
				sys.exit()
			elif event.key == pygame.K_SPACE:
				self._file_bullet()
	
	def _check_keyup_events(self,event):
		#��Ӧ�ɿ�
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False
	
	def _file_bullet(self):
		#����һ���ӵ���������������bullets��
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)
	
	def _update_screen(self):
		#������Ļ�ϵ�ͼ�񣬲��л�������Ļ
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)
		
		#��ʾ�÷�
		self.sb.show_score()
		
		#�����Ϸ���ڷǻ״̬���ͻ���Play��ť
		if not self.stats.game_active:
			self.play_button.draw_button()
		
		pygame.display.flip()

if __name__ == '__main__':
	#������Ϸʵ����������Ϸ
	ai = AlienInvasion()
	ai.run_game()
