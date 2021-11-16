#*coding:utf-8*
class GameStats:
	#������Ϸ��ͳ����Ϣ
	def __init__(self,ai_game):
		#��ʼ��ͳ����Ϣ
		self.settings = ai_game.settings
		self.reset_stats()
		#��Ϸһ��ʼ���ڷǻ״̬
		self.game_active = False
		#�κ�����¶���Ӧ��������ߵ÷�
		self.high_score = 0
	
	def reset_stats(self):
		#��ʼ������Ϸ�����ڼ���ܱ仯��ͳ����Ϣ
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1
