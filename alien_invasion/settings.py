#*coding:utf-8*
class Settings:
	#�洢��Ϸ�����������֡����������õ���
	
	def __init__(self):
		#��ʼ����Ϸ�ľ�̬����
		#��Ļ����
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		
		#�ɴ�����
		self.ship_limit = 3
		
		#�ӵ�����
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60,60,60
		self.bullets_allowed = 3
		
		#����������
		self.fleet_drop_speed = 10
		
		#�ӿ���Ϸ�Ľ���
		self.speedup_scale = 1.02
		#�����˷���������ٶ�
		self.score_scale = 1.2
		
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		#��ʼ������Ϸ���ж��仯������
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0
		
		#fleet_directionΪ1��ʾ���ң�Ϊ-1��ʾ����
		self.fleet_direction = 1
		
		#�Ʒ�
		self.alien_points = 50
	
	def increase_speed(self):
		#����ٶ����ú������˷���
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)
