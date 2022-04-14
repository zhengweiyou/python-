import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen            #将屏幕赋给了Ship的一个属性
        self.settings = ai_game.settings        #添加属性settings，在update()中使用它
        self.screen_rect = ai_game.screen.get_rect()        #使用方法get_rect()访问屏幕的属性rect，并将其赋给了self.screen_rect

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('C:\\untitled7\\alien_invasion\\imges\\ship2.png').convert_alpha()      #pygame.image.load()加载图像，并将图像的位置传递给它
        self.rect = self.image.get_rect()

        # 对于每艘新飞船，都将其放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x中存储小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up  = False
        self.moving_down = False

        # 空格和发射标志
        self.space = False
        self._bullets_fire = True

    def update(self):
        """根据移动标志调整飞船的位置"""
        #更新飞船而不是rect对象的x值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # 根据self.x更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y


    def blitme(self):       #定义了方法blitme(),它将图像绘制到self.rect指定的位置
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕底端居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
