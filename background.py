import pygame


class BackGrounds():

    def __init__(self, global_set, screen):
        super().__init__()
        #  初始化背景并设置其初始位置
        self.screen = screen
        self.global_set = global_set
        #  加载背景图像并获取其外接矩形
        self.image = pygame.image.load('images/background.jpg').convert()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

    def blitme(self):
        # 在指定位置绘制背景
        self.screen.blit(self.image, (0, 0))

