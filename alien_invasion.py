# 导入模块sys和pygame
import sys      # 使用sys中的工具来退出游戏
from time import sleep      # 从Python标准库的模块time中导入函数sleep()

import pygame   # 模块pygame包含开发游戏所需的功能

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()       # 初始化背景设置
        # 用Settings的实例作为AlienInvasion的属性settings
        self.settings = Settings()
        pygame.time.set_timer(self.settings.FIRE_EVENT, 100)
        # 传入尺寸（0，0）以及参数pygame.FULLSCREEN 生成一个覆盖整个显示器的屏幕
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.backgroud = pygame.image.load('C:\\untitled7\\alien_invasion\imges\\bg.jpg').convert()
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # 创建一个用于存储游戏统计信息的实例
        # 并创建记分牌
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()       # 创建用于存储子弹的编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()        # 创建一群外星人
        # 创建Play按钮
        self.play_button = Button(self, "Play Game")

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()        # 检查玩家输入

            if self.stats.game_active:
                self.ship.update()          # 更新飞船位置
                # self.bullets.update()     # 编组自动对其中的每个精灵调用update()
                self._update_bullets()      # 更新所有未消失子弹的位置
                self._update_aliens()

            self._update_screen()       # 使用更新的位置来绘制新屏幕

    def _check_events(self):        #检测相关的事件（如按下和松开键盘）
        """响应按键和鼠标事件"""
        # 事件循环  事件是用户玩游戏时执行的操作，如按键或移动鼠标
        for event in pygame.event.get():
            key_press = pygame.key.get_pressed()
            if key_press[pygame.K_SPACE]:
                """创建一颗子弹，并将其加入编组bullets中"""
                if len(self.bullets) < self.settings.bullets_allowed and event.type == self.settings.FIRE_EVENT:
                    new_bullet = Bullet(self)
                    self.bullets.add(new_bullet)
            # 当玩家单击游戏窗口的关闭按钮时，将检测到pygame.QUIT事件
            if event.type == pygame.QUIT:
                sys.exit()      #退出游戏
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
            """在玩家单击Play按钮时开始游戏"""
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.stats.game_active:
                # 重置游戏设置
                self.settings.initialize_dynamic_settings()
                self._start_game()

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:       #按Esc键退出游戏
            sys.exit()
        # elif event.key == pygame.K_SPACE:
        #     self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_i:
            self._pause_game()
        elif event.key == pygame.K_u:
            self._continute_game()

        # elif event.key == pygame.K_SPACE:    # 增加判断空格键响应
        #     self.ship.space = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

        # elif event.key == pygame.K_SPACE:
        #     self.ship.space = False


    def _start_game(self):
        """开始游戏"""
        # 重置游戏信息
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # 清空余下的外星人和子弹
        self.aliens.empty()
        self.bullets.empty()

        # 创建一群新的外星人并让飞船居中
        self._create_fleet()
        self.ship.center_ship()

        # 隐藏鼠标光标
        # 通过向set_visible()传递False,让Pygame在光标位于游戏窗口内时将其隐藏起来
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)       #创建一个Bullet实例并将其赋给new_bullet
            self.bullets.add(new_bullet)     #使用方法add()将其加入编组bullets中

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹"""
        #更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹
        # 使用for循环遍历列表时，python要求该列表的长度在整个循环中保持不变。
        # 因此不能从for循环遍历的列表中删除元素，必须遍历编组的副本。
        # 使用copy()来设置for循环，从而能够在循环中修改bullet
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:  # 检查每颗子弹，看看它是否从屏幕顶端消失
                self.bullets.remove(bullet)  # 如果是，则从bullet中删除remove()

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 删除发生碰撞的子弹和外星人
        # 将self.bullets中所有子弹与self.aliens中所有外星人进行比较，看它们是否重叠在一起。
        # 重叠时，groupcollide()就在它返回的字典中添加一个键值对。
        collisions = pygame.sprite.groupcollide(
                   self.bullets, self.aliens, True, True)
        # 两个实参True让pygame删除发生碰撞的子弹和外星人
        # 将第一个布尔实参设置为False，保留第二个True 模拟高能子弹，直到抵达屏幕顶部后消失

        if collisions:
            # 如果字典存在，就遍历其中所有的值，每个值都是一个列表，包含被同一颗子弹击中的所有外星人
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            # # 有子弹击中外星人时，返回一个字典（collisons）。如果存在字典，加分
            # self.stats.score += self.settings.alien_points
            # 调用prep_score()来创建一幅包含最新得分的新画像
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:  # 检查编组aliens是否为空，空编组相当于False
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()  # 调用_create_fleet()，在屏幕上重新显示一群外星人
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

        # print(len(self.bullets))  # 显示当前还有多少颗子弹，以核实确实删除了消失的子弹
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人

    def _update_aliens(self):
        """检查是否有外星人位于屏幕边缘。
        并更新整群外星人的位置"""
        self._check_fleet_edges()
        # 如果字典存在，就遍历其中所有的值，每个值都是一个列表，包含被同一颗子弹击中的所有外星人
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        # 函数spritecollideany接受两个实参：一个精灵和一个编组。
        # 它检查编组是否有成员与精灵发生碰撞，并在找到与精灵发生碰撞的成员后停止遍历编组。
        # 遍历编组aliens，并返回找到的第一个与飞船发生碰撞的外星人
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人宽度
        alien = Alien(self)     # 创建一个外星人
        # 需要知到外星人的宽度和高度，使用属性size，包含rect对象的宽度和高度
        alien_width, alien_height = alien.rect.size
        # 从外星人的rect属性中获取外星人宽度，并将这个值存储到alien_width中
        # 屏幕两边都留下一定的边距（将其设置为外星人的宽度）
        alien_width = alien.rect.width
        # 可用与放置外星人的水平空间为屏幕宽度减去两倍外星人宽度的两倍
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # //整除运算符，它将两个数相除并丢弃余数 显示一个外星人所需的水平空间为外星人宽度的两倍
        # 为确定一行可容纳多少个外星人，将可用空间除以外星人宽度的两倍
        number_alien_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        # 将计算公式用圆括号括起来，以便将代码分成两行，遵循每行不超过79字符的建议
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)

        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        # 为创建多行外星人，使用了两个嵌套在一起的循环，一个外部循环和一个内部循环
        # 外部循环从零数到要创建的外星人行数，重复次数为number_rows
        for row_number in range(number_rows):
            #创建第一行外星人
            for alien_number in range(number_alien_x):     # 内部循环创建一行外星人
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
            """创建一个外星人并将其加入当前行"""
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            alien_width = alien.rect.width      # 在内部获取外星人的宽度
            # 通过设置x坐标将其加入当前行
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x      # 使用外星人的属性x来设置其rect的位置
            # 在第一行外星人上方留出与外星人等高的空白区域，相邻外星人行的y坐标相差外星人的两倍
            # 因此将外星人高度乘以2，在乘以行号
            # 第一行的行号为0，因此第一行的垂直位置不变，而其他行都沿屏幕依次向下放置
            alien.rect.y = (alien.rect.height +
                            (2 * alien.rect.height * row_number))
            self.aliens.add(alien)      # 将每个新创建的外星人都添加到编组alens中

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取的相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将ships_left减1并更新记分牌
            self.stats.ships_left -= 1      # 飞船被外星人撞到，飞船数减1
            self.sb.prep_ships()
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            # 游戏结束后，在游戏进入非游戏状态后，立即让光标可见
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞一样处理
                self._ship_hit()
                break

    def _pause_game(self):
        """暂停游戏"""
        self.stats.game_active = False

    def _continute_game(self):
        """继续游戏"""
        self.stats.game_active = True

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.backgroud, (0,0))
        self.ship.blitme()  # 调用ship.blitme()将飞船绘制到屏幕上，确保它出现在背景前面
        # 方法bullet.sprites()返回一个列表，其中包含bullets中的所有精灵
        for bullet in self.bullets.sprites():
            # 遍历编组bullets的精灵，并对每一个精灵调用draw_bullet()
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        #每次循环时都重绘屏幕
        # self.screen.fill(self.bg_color)     #调用方法fill() 用背景色填充屏幕


        #让最近绘制的屏幕可见
        # 不断更新屏幕，显示元素的新位置，在原来的位置隐藏元素，营造平滑移动的效果
        # self.backgroud.blit(self.backgroud, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()