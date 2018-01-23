import pygame
from pygame.sprite import Sprite
import math


class Bullet(Sprite):
    #  一个对飞船发射的子弹进行管理的类
    def __init__(self, global_set, screen, little_cute):
        #  在飞船所处的位置创建一个子弹对象
        super().__init__()
        self.screen = screen
        self.global_set = global_set
        #  加载子弹声音
        self.audio = 'audio/biu.wav'
        #  加载子弹图像，并设置其 rect 属性
        self.image = pygame.image.load('images/timg.png').convert_alpha()
        self.rect = self.image.get_rect()
        #  设置正确的位置
        self.rect.centerx = little_cute.rect.centerx
        self.rect.top = little_cute.rect.top
        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.color = global_set.bullet_color
        self.bullet_speed_factor = global_set.bullet_speed_factor
        #  火花爆炸序号
        self.explode_index = 0
        self.explode_index_float = 0
        self.initial_fire()

    def initial_fire(self):
        #  读取火花图像序列
        fire_img = pygame.image.load('images/fire_seq.png').convert_alpha()
        self.fire_surface = list()
        self.fire_surface.append(fire_img.subsurface(pygame.Rect(0, 0, 40, 40)))
        self.fire_surface.append(fire_img.subsurface(pygame.Rect(40, 0, 40, 40)))
        self.fire_surface.append(fire_img.subsurface(pygame.Rect(80, 0, 40, 40)))
        self.fire_surface.append(fire_img.subsurface(pygame.Rect(120, 0, 40, 40)))
        self.fire_surface.append(fire_img.subsurface(pygame.Rect(160, 0, 40, 40)))
        self.fire_surface.append(fire_img.subsurface(pygame.Rect(200, 0, 40, 40)))
        self.fire_surface.append(fire_img.subsurface(pygame.Rect(240, 0, 40, 40)))
        self.fire_surface.append(fire_img.subsurface(pygame.Rect(280, 0, 40, 40)))
        #  确定火花位置
        self.fire_rect = self.fire_surface[1].get_rect()
        self.fire_rect.centerx = self.rect.centerx

    def blitme(self):
        #  确定火花位置
        self.fire_rect.centery = self.rect.top
        #  在指定位置绘制火花
        self.screen.blit(self.fire_surface[self.explode_index], self.fire_rect)

    def update_fire(self):
        #  更新爆炸图序列
        self.explode_index_float += 0.1
        self.explode_index = math.floor(self.explode_index_float)

    def update(self):
        #  向上移动子弹
        #  更新表示子弹位置的小数值
        self.y -= self.bullet_speed_factor
        # 更新表示子弹的 rect 的位置
        self.rect.y = self.y

    def draw_bullet(self):
        #  在屏幕上绘制子弹
        self.screen.blit(self.image, self.rect)

    def suondme(self):
        sound = pygame.mixer.Sound(self.audio)
        sound.play()

