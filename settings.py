class Settings:
    """与AlienInvasion设置有关的类"""
    
    def __init__(self):
        """初始化游戏的设置"""

        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #飞船设置
        self.ship_number = 3

        #子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3

        #外星人设置
        self.fleet_drop_speed = 10

        #加快游戏节奏的速度
        self.speed_up_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""

        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 1.0

        #外星人群移动方向，1为右，-1为左
        self.fleet_direction = 1

        #计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置"""

        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale
        #为了让分数为整数，用int转化
        self.alien_points = int(self.alien_points * self.speed_up_scale)