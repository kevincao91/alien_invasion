import pygame
import pygame.font
from pygame.sprite import Group
from shipscoreboard import ShipScoreBoard


class Scoreboards():
    #  显示得分信息的类
    def __init__(self, global_set, screen, stats):
        #  初始化显示得分涉及的属性
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.global_set = global_set
        self.stats = stats
        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 32)
        #  确定分数栏高度、宽度、背景色
        self.score_bar_height = 50
        self.score_bar_width = self.screen_rect.width
        self.score_bar_bg_color = (180, 180, 255)
        self.get_score_bar_height()
        #  确定血条高度、宽度
        self.hp_image = pygame.image.load('images/hp.png').convert_alpha()
        self.hp_bg_image = pygame.image.load('images/hp_bg.png').convert_alpha()
        self.hp_rect = self.hp_bg_image.get_rect()
        self.hp_ori_rect_width = self.hp_rect.width
        self.hp_ori_rect_height = self.hp_rect.height
        self.hp_bg_rect = self.hp_bg_image.get_rect()
        #  准备分数栏图片，仅初始化时生成一次
        self.prep_score_bar()
        # 准备包含最高得分、当前得分、等级和飞船数的图像
        self.prep_images()

    def get_score_bar_height(self):
        self.high_test_image = self.font.render("Test_Height", True, self.text_color, self.global_set.bg_color)
        self.high_test_rect = self.high_test_image.get_rect()
        self.score_bar_height = self.high_test_rect.height * 1.5
        self.global_set.score_bar_height = self.score_bar_height

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score_bar(self):
        #  准备分数栏图片
        #  创建按钮的 rect 对象，并使其居中
        self.score_bar_rect = pygame.Rect(0, 0, self.score_bar_width, self.score_bar_height)
        self.score_bar_rect.center = self.screen_rect.center
        self.score_bar_rect.top = self.screen_rect.top

    def prep_score(self):
        #  将得分转换为一幅渲染的图像
        #  取整
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        score_str = 'Score:' + score_str
        self.score_image = self.font.render(score_str, True, self.text_color, self.score_bar_bg_color)
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centery = self.score_bar_rect.centery
        self.score_rect.right = self.screen_rect.right - 20

    def show_score(self):
        #  在屏幕上显示当前得分、最高得分、等级和飞船数
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        #  判断是否显示boss血条
        if self.stats.is_boss:
            self.prep_boss_hp()
            self.screen.blit(self.hp_bg_image, self.hp_bg_rect)
            self.screen.blit(self.hp_surface, self.hp_surface_rect)

    def prep_high_score(self):
        #  将最高得分转换为渲染的图像
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        high_score_str = 'Best:' + high_score_str
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.score_bar_bg_color)
        # 将最高得分放在分数栏中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.centery = self.score_bar_rect.centery

    def prep_level(self):
        #  将等级转换为渲染的图像
        alien_level_str = 'Level:' + str(self.stats.level)
        self.level_image = self.font.render(alien_level_str, True, self.text_color, self.score_bar_bg_color)
        # 将等级放在得分左方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right - 160
        self.level_rect.centery = self.score_bar_rect.centery

    def prep_ships(self):
        #  显示还余下多少艘飞船
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = ShipScoreBoard(self.global_set, self.screen)
            ship.rect.centery = self.score_bar_rect.centery
            ship.rect.x = 10 + ship_number * (ship.rect.width + 5)
            self.ships.add(ship)

    def prep_boss_hp(self):
        #  显示boss血量
        #  根据血量调整长度
        hp_rect_width = self.hp_ori_rect_width * self.stats.boss_HP / self.global_set.MAX_HP
        self.hp_surface = self.hp_image.subsurface(pygame.Rect(0, 0, int(hp_rect_width), self.hp_ori_rect_height))
        self.hp_surface_rect = self.hp_surface.get_rect()
        #  将等级放在飞船数右方
        self.hp_surface_rect.left = 160
        self.hp_surface_rect.centery = self.score_bar_rect.centery
        #  血条背景
        self.hp_bg_rect.left = 160
        self.hp_bg_rect.centery = self.score_bar_rect.centery



