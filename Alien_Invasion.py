import sys
import pygame

from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""

        pygame.init()
        #创建Settings类的对象实例，通过该对象管理窗口设置
        self.settings = Settings()

        #创建游戏窗口和窗口标题
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #全屏运行游戏，请确认设计了退出方式，因为Pygame默认不提供在全屏模式下退出游戏的方式
        #self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        #pygame.display.set_caption("Alien Invasion")

        #创建存储游戏统计信息的实例
        self.stats = GameStats(self)
        #创建计分牌
        self.score_board = Scoreboard(self)
        #创造并绘制飞船
        self.ship = Ship(self)
        #创建存储子弹的编组
        self.bullets = pygame.sprite.Group()
        #创造外星人
        self.aliens = pygame.sprite.Group()
        self.create_fleet()
        #创建Play按钮
        self.play_button = Button(self,"Play")

    def run_game(self):
        """开始游戏循环的主体"""

        while True:
            self.check_events()

            if self.stats.game_active:
                self.ship.update()
                self.update_bullet()
                self.update_aliens()
            
            self.update_screen()

    def check_events(self):
        """响应鼠标和键盘按键"""

        for event in pygame.event.get():
            #退出游戏
            if event.type == pygame.QUIT:
                sys.exit()
            #飞船行动 
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def check_play_button(self,mouse_pos):
        """在玩家单机play按钮时开始新游戏"""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            #重置游戏统计信息
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.score_board.prep_score()
            self.score_board.prep_level()
            self.score_board.prep_ships()
            #隐藏鼠标光标
            pygame.mouse.set_visible(False)

            #清空剩下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底部的中央
            self.create_fleet()
            self.ship.center_ship()

    def check_keydown_events(self,event):
        """响应按键"""

        #左右移动
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #按q键退出
        elif event.key == pygame.K_q:
            sys.exit()
        #发射子弹
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def check_keyup_events(self,event):
        """响应按键松开"""

        #左右移动
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullet(self):
        """更新子弹的位置，并删除屏幕之外的子弹"""

        #更新子弹的位置
        self.bullets.update()

        #删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""

        #检查是否有子弹击中了外星人。
        #如果是，就删除响应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        #当有外星人被击落时，更新得分
        if collisions:
            #防止一颗子弹击中多个外星人，却只计一次分，遍历，用少掉的外星人数计分
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.score_board.prep_score()
            self.score_board.check_high_score()
        
        #若外星人全部被消灭，就建立新的外星人群
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level += 1
            self.score_board.prep_level()

    def create_alien(self,alien_number,row_number):
        """创造一个外星人并将其放入当前行"""

        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.y = alien_height + 2 *alien_height * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)
            
    def create_fleet(self):
        """创建外星人群"""

        #创建一个外星人，并计算一行可容纳多少外星人
        #外星人间距为外星人宽度
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #计算屏幕能容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        #创建外星人群
        for row_number in range(number_rows):
            #创建第一行外星人
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number,row_number)

    def check_fleet_edges(self):
        """当外星人到达边缘时采取相应的措施"""

        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""

        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""

        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self.game_stats_change()
                break

    def update_aliens(self):
        """更新外星人群中所有外星人的位置"""

        self.check_fleet_edges()
        self.aliens.update()

        #检测飞船与外星人的碰撞
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self.game_stats_change()

        #检测是否有外星人到达了屏幕底端
        self.check_aliens_bottom()

    def game_stats_change(self):
        """外星人撞上飞船或到达底部之后做的处理"""

        if self.stats.ships_left > 0:
             #将飞船剩余数目-1
            self.stats.ships_left -= 1
            self.score_board.prep_ships()

            #清空剩下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底部的中央
            self.create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update_screen(self):
        """更新屏幕，并使其可见"""

        #重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        #子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #外星人
        self.aliens.draw(self.screen)

        #显示得分
        self.score_board.show_score()

        #如果游戏处于非活动状态，就绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        #让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    #创建游戏实例并运行游戏

    ai = AlienInvasion()
    ai.run_game()
    