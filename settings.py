"""一个给游戏添加新功能的模块"""
import pygame

class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        self.FIRE_EVENT = pygame.USEREVENT      #设置开火常量
        # 屏幕设置
        self.screen_width = 1300
        self.screen_height = 700
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 1.5  # 控制飞船速度
        self.ship_limit = 3

        # 子弹设置（创建宽3像素，高15像素的深灰色子弹，子弹速度比飞船稍低）
        self.bullet_speed = 10
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 100       # 子弹数量


        # 外星人设置
        self.alien_speed = 0.5
        self.fleet_drop_speed = 5

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度设置和外星人分数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
        # 确认分数在不断增加后，一定要删除调用函数print()的代码
        # 否则可能会影响游戏的性能，分散玩家的注意力