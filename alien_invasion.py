

import pygame
from setting import Settings
from ship import Ships
from alien import Aliens
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Buttons
from scoreboard import Scoreboards


def run_game():
    #  初始化游戏并创建一个屏幕对象
    pygame.init()
    global_set = Settings()

    screen = pygame.display.set_mode((global_set.screen_width, global_set.screen_height))
    pygame.display.set_caption(global_set.game_title)

    #  创建 Play 按钮
    play_button = Buttons(global_set, screen, "Play")

    #  创建一个用于存储游戏统计信息的实例
    stats = GameStats(global_set)
    #  创建记分牌
    score_board = Scoreboards(global_set, screen, stats)
    #  创建一艘飞船
    ship = Ships(global_set, screen)
    #  创建一个用于存储子弹的编组
    bullets = Group()
    #  创建一个用于储存外星人的编组
    aliens = Group()

    #  创建外星人群
    gf.create_fleet(global_set, screen, ship, aliens)

    #  开始游戏的主循环
    while True:
        #  监视键盘和鼠标事件
        gf.check_events(global_set, screen, stats, score_board, play_button, ship, aliens, bullets)

        if stats.game_active:
            #  事物更新
            ship.update()
            gf.update_bullets(global_set, stats, screen, score_board, ship, aliens, bullets)
            gf.update_aliens(global_set, stats, screen, score_board, ship, aliens, bullets)

        #  每次循环时都重绘屏幕
        gf.update_screen(global_set, stats, screen, score_board, ship, aliens, bullets, play_button)


run_game()
