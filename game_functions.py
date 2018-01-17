import sys
import pygame
from bullet import Bullet
from alien import Aliens
from time import sleep
import json


def check_full_screen(global_set):
    global_set.window_width = pygame.display.Info().current_w
    global_set.window_height = pygame.display.Info().current_h
    #  是否全屏
    if global_set.full_screen:
        global_set.flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        global_set.screen_width = global_set.window_width
        global_set.screen_height = global_set.window_height
    else:
        global_set.flags = 0


def check_keydown_events(event, stats, screen, global_set, score_board, ship, aliens, bullets):
    # 响应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(global_set, screen, ship, bullets)
    elif event.key == pygame.K_q:
        quit_game(stats, global_set)
    elif event.key == pygame.K_RETURN:
        check_enter_button(global_set, screen, stats, score_board, ship, aliens, bullets)


def quit_game(stats, global_set):
    with open(global_set.info_file, 'w') as fileobject:
        json.dump(stats.high_score, fileobject)
    sys.exit()


def check_keyup_events(event, ship):
    #  响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def initialize_and_start_game(global_set, screen, stats, score_board, aliens, ship, bullets):
    # 重置游戏设置
    global_set.initialize_dynamic_settings()
    # 隐藏光标
    pygame.mouse.set_visible(False)
    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    # 重置记分牌图像
    score_board.prep_images()
    #  清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    #  创建一群新的外星人，并让飞船居中
    create_fleet(global_set, screen, score_board, ship, aliens)
    ship.center_ship()


def check_enter_button(global_set, screen, stats, score_board, ship, aliens, bullets):
    #  在玩家单击Enter按钮时等价于点击play button
    if not stats.game_active:
        # 初始化并开始游戏
        initialize_and_start_game(global_set, screen, stats, score_board, aliens, ship, bullets)


def check_play_button(global_set, screen, stats, score_board, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    #  在玩家单击 Play 按钮时开始新游戏
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        if not stats.game_active:
            # 初始化并开始游戏
            initialize_and_start_game(global_set, screen, stats, score_board, aliens, ship, bullets)


def check_events(global_set, screen, stats, score_board, play_button, ship, aliens, bullets):
    #  响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, stats, screen, global_set, score_board, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(global_set, screen, stats, score_board, play_button, ship, aliens, bullets, mouse_x,
                              mouse_y)


def update_screen(global_set, stats, screen, score_board, ship, aliens, bullets, play_button):
    #  更新屏幕上的图像，并切换到新屏幕
    #  每次循环时都重绘屏幕
    #  1、最底层  背景色
    screen.fill(global_set.bg_color)
    #  2、绘制外星人群
    aliens.draw(screen)
    #  3、在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #  4、绘制飞船
    ship.blitme()
    #  5、绘制分数栏
    screen.fill(score_board.score_bar_bg_color, score_board.score_bar_rect)
    #  6、显示得分
    score_board.show_score()
    #  7、如果游戏处于非活动状态，就绘制 Play 按钮
    if not stats.game_active:
        play_button.draw_button()

    #  让最近绘制的屏幕可见
    pygame.display.flip()


def check_high_score(stats, score_board):
    #  检查是否诞生了新的最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()


def check_bullet_alien_collisions(global_set, stats, screen, score_board, ship, aliens, bullets):
    #  响应子弹和外星人的碰撞
    #  删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # 计算碰撞字典中碰撞个数并计算得分
        for liens in collisions.values():
            stats.score += global_set.alien_points * len(liens)
        score_board.prep_score()
        check_high_score(stats, score_board)

    if len(aliens) == 0:
        start_new_level(global_set, screen, stats, score_board, ship, aliens, bullets)


def start_new_level(global_set, screen, stats, score_board, ship, aliens, bullets):
    #  删除现有的所有子弹，并创建一个新的外星人群
    bullets.empty()
    global_set.increase_speed()
    create_fleet(global_set, screen, score_board, ship, aliens)
    # 提高等级
    stats.level += 1
    score_board.prep_level()


def update_bullets(global_set, stats, screen, score_board, ship, aliens, bullets):
    #  更新子弹的位置
    bullets.update()
    #  删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= score_board.score_bar_height:
            bullets.remove(bullet)
    check_bullet_alien_collisions(global_set, stats, screen, score_board, ship, aliens, bullets)


def fire_bullet(global_set, screen, ship, bullets):
    #  如果还没有到达限制，就发射一颗子弹
    #  创建一颗子弹，并将其加入到编组 bullets 中
    if len(bullets) < global_set.bullets_allowed:
        new_bullet = Bullet(global_set, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(global_set, alien_width):
    #  计算每行可容纳多少个外星人
    available_space_x = global_set.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(global_set, score_board, ship_height, alien_height):
    #  计算屏幕可容纳多少行外星人
    available_space_y = (global_set.screen_height - score_board.score_bar_height - ship_height) * \
                        global_set.alien_high_fill_factor
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(global_set, screen, score_board, aliens, alien_number, row_number):
    #  创建一个外星人并将其放在当前行
    alien = Aliens(global_set, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = score_board.score_bar_height + alien.rect.height * 0.5 + 2 * alien.rect.height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)


def create_fleet(global_set, screen, score_board, ship, aliens):
    #  创建外星人群
    #  创建一个外星人，并计算每行可容纳多少个外星人
    alien = Aliens(global_set, screen)
    number_aliens_x = get_number_aliens_x(global_set, alien.rect.width)
    number_rows = get_number_rows(global_set, score_board, ship.rect.height, alien.rect.height)
    #  创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(global_set, screen, score_board, aliens, alien_number, row_number)


def check_fleet_edges(global_set, aliens):
    #  有外星人到达边缘时采取相应的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(global_set, aliens)
            break


def change_fleet_direction(global_set, aliens):
    #  将整群外星人下移，并改变它们的方向
    for alien in aliens.sprites():
        alien.rect.y += global_set.fleet_drop_speed
    global_set.fleet_direction *= -1


def ship_hit(global_set, stats, screen, score_board, ship, aliens, bullets):
    #  响应被外星人撞到的飞船
    #  将 ships_left 减 1
    stats.ships_left -= 1
    # 更新记分牌
    score_board.prep_ships()

    if stats.ships_left > 0:
        #  清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #  创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(global_set, screen, score_board, ship, aliens)
        ship.center_ship()
        #  暂停
        sleep(0.5)
    else:
        stats.game_active = False
        # 光标可见
        pygame.mouse.set_visible(True)


def check_aliens_bottom(global_set, stats, screen, score_board, ship, aliens, bullets):
    #  检查是否有外星人到达了屏幕底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #  像飞船被撞到一样进行处理
            ship_hit(global_set, stats, screen, score_board, ship, aliens, bullets)
            break


def update_aliens(global_set, stats, screen, score_board, ship, aliens, bullets):
    #  更新外星人群中所有外星人的位置
    #  检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    check_fleet_edges(global_set, aliens)
    aliens.update()
    #  检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(global_set, stats, screen, score_board, ship, aliens, bullets)
    #  检查是否有外星人到达屏幕底端
    check_aliens_bottom(global_set, stats, screen, score_board, ship, aliens, bullets)
