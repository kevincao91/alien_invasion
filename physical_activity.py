import pygame
import random
import sys
from setting import Settings
from alien_boss import AlienBosses
from pygame.sprite import Group


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


def check_keydown_events(event):
    # 响应按键
    if event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_events():
    #  响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event)


def update_screen(global_set, screen, bosses):
    #  更新屏幕上的图像，并切换到新屏幕
    #  每次循环时都重绘屏幕
    #  1、最底层  背景色
    screen.fill(global_set.bg_color)
    #  测试boss
    for boss in bosses.sprites():
        boss.blitme()
    #  让最近绘制的屏幕可见
    pygame.display.flip()
    #  pygame.display.update()


def create_boss(global_set, screen, stats, bosses, alien_number):
    #  创建一个外星人boos
    alien_boss = AlienBosses(global_set, screen, alien_number)
    #  初始随机位置
    alien_boss.initial_position()
    bosses.add(alien_boss)


def update_bosses(bosses):
    for boss in bosses.sprites():
        boss.update()


def check_boss_edges(global_set, bosses):            #  写他
    #  有外星人到达边缘时采取相应的措施
    for boss in bosses.sprites():
        if boss.check_edges():
            change_fleet_direction(global_set, boss)
            break


def test():
    #  pygame初始化
    pygame.init()
    global_set = Settings()
    screen = pygame.display.set_mode((global_set.screen_width, global_set.screen_height), global_set.flags)
    #  创建一个用于储存外星人boos的编组
    bosses = Group()
    create_boss(global_set, screen, 1, bosses, 1)
    while True:
        #  响应按键和鼠标事件
        check_events()
        update_bosses(bosses)
        #  更新屏幕上的图像，并切换到新屏幕
        update_screen(global_set, screen, bosses)



# =========

test()
