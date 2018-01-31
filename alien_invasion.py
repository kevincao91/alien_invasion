import pygame
from setting import Settings
from ship import Ships
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Buttons
from scoreboard import Scoreboards
from background import BackGrounds
from mousecursor import MouseCursors
import os


def run_game():
    #  初始化游戏并创建一个屏幕对象
    # 定义时钟
    clock = pygame.time.Clock()
    #  pygame初始化
    pygame.init()
    pygame.mixer.init()
    #  加载背景音乐
    pygame.mixer.music.load(os.path.relpath('audio/BGM.mp3'))
    pygame.mixer.music.play(-1, 0.0)
    pygame.time.delay(1000)  # 等待1秒让mixer完成初始化
    global_set = Settings()
    #  设置全屏参数
    gf.check_full_screen(global_set)
    screen = pygame.display.set_mode((global_set.screen_width, global_set.screen_height), global_set.flags)
    #  设置标题
    pygame.display.set_caption(global_set.game_title)
    #  创建背景图
    back_ground = BackGrounds(global_set, screen)
    if global_set.full_screen:
        back_ground.image = pygame.transform.scale(back_ground.image, (global_set.screen_width, global_set.screen_height))
    #  创建鼠标图
    mouse_cursor = MouseCursors(global_set, screen)
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
    #  创建一个用于储存外星人boos的编组
    bosses = Group()
    #  创建一个用于储存火花的编组
    fires = Group()
    #  创建外星人群
    gf.create_fleet(global_set, screen, stats, score_board, ship, aliens, bosses)
    #  开始游戏的主循环
    while True:
        #  控制游戏最大帧率归零
        clock.tick(global_set.FRAME_RATE)
        #  画面帧标示
        if global_set.ticks >= global_set.ANIMATE_CYCLE:
            global_set.ticks = 0
        #  监视键盘和鼠标事件
        gf.check_events(global_set, screen, stats, score_board, play_button, ship, aliens, bullets, mouse_cursor, bosses)

        if stats.game_state:
            #  游戏事物更新控制
            gf.game_state_control(global_set, stats, screen, score_board, ship, aliens, bullets)
            #  能否移动飞船
            if not stats.ship_freeze_flag:
                ship.update()
            #  能否移动外星人和子弹
            if not stats.aliens_bullet_freeze_flag:
                gf.update_aliens(global_set, stats, screen, score_board, ship, aliens)
                gf.update_bullets(global_set, stats, screen, score_board, ship, aliens, bullets, fires)
            #  更新火花
            if fires:
                gf.update_fires(fires)
        #  每次循环时都重绘屏幕
        gf.update_screen(back_ground, mouse_cursor, stats, screen, score_board, ship, aliens, bullets, play_button,
                         fires, bosses)
        # ticks + 1
        global_set.ticks += 1

# ======================================================================================================================


run_game()
