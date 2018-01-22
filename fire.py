import pygame
from pygame.sprite import Sprite


class Fires(Sprite):
    #  一个对子弹产生的火花进行管理的类
    def __init__(self, global_set, screen, bullet):
        #  在子弹所处的位置创建一个火花对象
        super().__init__()
        self.screen = screen
        #  加载子弹声音
        self.audio = 'audio/biu.wav'
        #  加载火花图像，并设置其 rect 属性
        self.image = pygame.image.load('images/fire.png').convert_alpha()
        self.rect = self.image.get_rect()
        #  设置正确的位置
        self.rect.centerx = bullet.rect.centerx
        self.rect.top = bullet.rect.top
        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

    def draw_bullet(self):
        #  在屏幕上绘制子弹
        self.screen.blit(self.image, self.rect)

    def suondme(self):
        sound = pygame.mixer.Sound(self.audio)
        sound.play()

