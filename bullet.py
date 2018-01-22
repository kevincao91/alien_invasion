import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    #  一个对飞船发射的子弹进行管理的类
    def __init__(self, global_set, screen, little_cute):
        #  在飞船所处的位置创建一个子弹对象
        super().__init__()
        self.screen = screen
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

