# 导入模块pygame.font  它让Pygame能够将文本渲染到屏幕上
import pygame.font

class Button():

    def __init__(self, ai_game, msg):       # msg是要在按钮中显示的文本
        """初始化按钮属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)       # Sys.Font（默认字体, 48号）

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        # 调用font.render()将存储在msg中的文本转化为图像  接受一个布尔实参，开启/关闭反锯齿功能（反锯齿让文本边缘更平滑）
        self.msg_imge = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_imge_rect = self.msg_imge.get_rect()
        self.msg_imge_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，在绘制文本"""
        # 调用screen.fill()来绘制表示按钮的矩形
        self.screen.fill(self.button_color, self.rect)
        # 在调用screen.blit()向它传递一副画像以及与画像相关联的rect，在屏幕上绘制文本图像
        self.screen.blit(self.msg_imge, self.msg_imge_rect)