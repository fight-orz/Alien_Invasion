import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""

    #ai_game为指向当前AlienInvasion 实例的引用
    def __init__(self,ai_game):
        """初始化飞船并设置位置"""

        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #对于每艘新飞船，将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        #移动标志
        self.moving_right = False
        self.moving_left = False

        #在飞船的属性x中存储小数值
        self.x = float(self.rect.x)
        
    def blitme(self):
        """在指定位置绘制飞船"""

        self.screen.blit(self.image,self.rect)

    def update(self):
        """根据移动标志调整飞船的位置"""

        #若这里用if-elif的话，左移的优先级将会永远比右移小
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #根据ship.x更新rect对象
        self.rect.x = self.x

    def center_ship(self):
        """让飞船停在屏幕底部正中央"""

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)