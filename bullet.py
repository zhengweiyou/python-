import pygame
from pygame.sprite import Sprite
# 从模块pygame.sprite导入Sprite类
# 使用精灵（sprite),可将游戏中相关的元素编组，进而同时操作编组中的所有元素

class Bullet(Sprite):  # Bullet类继承Sprite类
    """管理飞船所发射子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()  # 调用super()来继承Sprite
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在（0，0）处创建一个表示子弹的矩形，在设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)  # 创建子弹的属性rect
        self.rect.midtop = ai_game.ship.rect.midtop  # 将子弹中的rect.midtop设置为飞船的rect.midtop，这样的子弹将从飞船的顶部发射

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)  # 将子弹的y坐标存储为小数值，以便能够微调子弹的速度

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed  
        # 更新表示子弹的rect位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
