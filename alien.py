import pygame
from pygame.sprite import Sprite
import pygame.locals


class Aliens(Sprite):
    #  表示单个外星人的类
    def __init__(self, global_set, screen, stats):
        # 初始化外星人并设置其起始位置
        super().__init__()
        self.screen = screen
        self.global_set = global_set
        #  加载外星人图像，并设置其 rect 属性
        self.image = pygame.image.load('images/bigpig.png').convert_alpha()
        self.rect = self.image.get_rect()
        #  每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width/2
        self.rect.y = self.rect.height/2
        #  存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


    def blitme(self):
        #  在指定位置绘制外星人
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        #  如果外星人位于屏幕边缘，就返回 True
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        #  向左或向右移动外星人
        self.x += (self.global_set.alien_speed_factor * self.global_set.fleet_direction)
        self.rect.x = self.x



