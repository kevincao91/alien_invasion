import pygame
from pygame.sprite import Sprite
import pygame.locals
import random
import math


class AlienBosses(Sprite):
    #  表示单个外星人的类
    def __init__(self, global_set, screen, stats):
        # 初始化外星人并设置其起始位置
        super().__init__()
        self.screen = screen
        self.global_set = global_set
        #  加载外星人图像，并设置其 rect 属性
        self.image = pygame.image.load('images/bigpig_boss.png').convert_alpha()
        self.rect = self.image.get_rect()
        #  每个外星人最初都在屏幕左上角
        self.rect.x = 0
        self.rect.y = 0
        #  存储外星人的准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        #  外星人boss游戏性设置
        #  初始速度、方向
        self.initial_speed = round(random.uniform(0, 1), 2)
        self.initial_speed_angle = round(random.uniform(180, 360))
        #  speed[x方向速度  y方向速度]
        self.speed_angle = self.initial_speed_angle
        self.speed = [self.initial_speed * math.cos(self.speed_angle), self.initial_speed * math.sin(self.speed_angle)]

        #  恒定加速度、初始加速度方向
        self.constant_acc = 1
        self.initial_acc_angle = round(random.uniform(180, 360))
        self.acc_angle = self.initial_acc_angle
        self.acc = [self.constant_acc * math.cos(self.acc_angle), self.constant_acc * math.sin(self.acc_angle)]

    def initial_position(self):
        self.y = float(self.rect.height / 20)
        self.x = float((self.global_set.screen_width - self.rect.width) * random.random())
        self.rect.x = self.x
        self.rect.y = self.y
        print(self.rect)

    def blitme(self):
        #  在指定位置绘制外星人boss
        self.screen.blit(self.image, self.rect)

    def check_edges(self):          #  写他
        #  如果外星人位于屏幕边缘，就返回 True
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        #
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.speed[0] += self.acc[0]
        self.speed[1] += self.acc[1]

        print([self.rect.x, self.rect.y])
        #  更新坐标值
        # self.rect.x = self.x
