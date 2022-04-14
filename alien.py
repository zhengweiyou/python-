import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #加载外星人图像并设置其rect属性
        self.image = pygame.image.load('C:\\untitled7\\alien_invasion\\imges\\alien3.png').convert_alpha()
        self.rect = self.image.get_rect()

        #每个外星人最初都在屏幕左上角附件
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人的精确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:     # 如果外星人的rect属性right大于或等于屏幕的rect的right属性，就说明外星人位于屏幕右边缘
            return True

    def update(self):
        """向左或向右移动外星人"""
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x
        # self.x += self.settings.alien_speed     # 使用属性self.x跟踪每个外星人的准确位置
        # self.rect.x = self.x                    # 使用self.x的值来更新外星人的rect位置