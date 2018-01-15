
import pygame
from setting import Settings
from ship import Ships
import game_functions as gf
from pygame.sprite import Group


def run_game():
    #  初始化游戏并创建一个屏幕对象
    pygame.init()
    global_set = Settings()

    screen = pygame.display.set_mode((global_set.screen_width, global_set.screen_height))
    pygame.display.set_caption(global_set.game_title)

    #  创建一艘飞船
    ship = Ships(global_set, screen)
    #  创建一个用于存储子弹的编组
    bullets = Group()

    #  开始游戏的主循环
    while True:
        #  监视键盘和鼠标事件
        gf.check_events(screen, global_set, ship, bullets)
        #  事物更新
        ship.update()
        gf.update_bullets(bullets)
        #  每次循环时都重绘屏幕
        gf.update_screen(global_set, screen, ship, bullets)


run_game()
