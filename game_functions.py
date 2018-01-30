import sys
import pygame
from bullet import Bullet
from alien import Aliens
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
    if event.key == pygame.K_q:
        quit_game(stats, global_set)
    elif event.key == pygame.K_ESCAPE:
        quit_game(stats, global_set)
    elif event.key == pygame.K_RETURN:
        check_enter_button(global_set, screen, stats, score_board, ship, aliens, bullets)
    elif stats.game_active:
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if not stats.aliens_bullet_freeze_flag:
                fire_bullet(global_set, screen, ship, bullets)


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


def play_read_go(global_set):
    global_set.begin_audio_channel = global_set.begin_audio.play()


def check_sound(global_set, stats):
    if stats.game_state in [1, 11]:
        if not global_set.begin_audio_channel.get_busy():
            stats.game_state = 2
    if stats.game_state == 3:
        if not global_set.ship_hit_audio_channel.get_busy():
            stats.game_state = 4


def game_state_control(global_set, stats, screen, score_board, ship, aliens, bullets):
    #  game_state值      游戏状态    飞船状态    外星人状态   子弹状态    对应阶段
    #  0                非激活状态   不可移动    不移动       不能产生  游戏未开始，等待开始阶段
    #  1                激活状态     不可移动    不移动       不能产生  准备开始，播放开始声音阶段
    #  11               激活状态     可移动      不移动       不能产生  新一级准备开始，播放开始声音阶段
    #  2                激活状态      可移动      移动         能产生   正常游戏阶段
    #  3                激活状态     不可移动    不移动       不能产生     坠机，播放坠机声音阶段
    #  4                激活状态     不可移动    不移动       不能产生   判断游戏是否继续阶段

    if stats.game_state == 0:
        stats.aliens_bullet_freeze_flag = True
        stats.ship_freeze_flag = True
        stats.game_active = False
    elif stats.game_state == 1:
        stats.game_active = True
        stats.aliens_bullet_freeze_flag = True
        stats.ship_freeze_flag = True
        check_sound(global_set, stats)
    elif stats.game_state == 11:
        stats.game_active = True
        stats.aliens_bullet_freeze_flag = True
        stats.ship_freeze_flag = False
        check_sound(global_set, stats)
    elif stats.game_state == 2:
        stats.game_active = True
        stats.aliens_bullet_freeze_flag = False
        stats.ship_freeze_flag = False
    elif stats.game_state == 3:
        stats.game_active = True
        stats.aliens_bullet_freeze_flag = True
        stats.ship_freeze_flag = True
        check_sound(global_set, stats)
    elif stats.game_state == 4:
        stats.game_active = True
        stats.aliens_bullet_freeze_flag = True
        stats.ship_freeze_flag = True
        #  判断下一步处理
        level_again_or_start_new_level(global_set, stats, screen, score_board, ship, aliens, bullets)


def initialize_and_start_game(global_set, screen, stats, score_board, aliens, ship, bullets):
    #  重置游戏设置
    global_set.initialize_dynamic_settings()
    #  隐藏光标
    pygame.mouse.set_visible(False)
    #  重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    #  重置记分牌图像
    score_board.prep_images()
    #  开始游戏
    start_game(global_set, screen, stats, score_board, aliens, ship, bullets)


def start_game(global_set, screen, stats, score_board, aliens, ship, bullets):
    #  开始游戏
    #  清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    #  创建一群新的外星人，并让飞船居中
    create_fleet(global_set, screen, stats, score_board, ship, aliens)
    ship.center_ship()
    #  播放开始音效
    play_read_go(global_set)
    #  更新游戏状态信息   等待开始声音结束
    stats.game_state = 1


def check_enter_button(global_set, screen, stats, score_board, ship, aliens, bullets):
    #  在玩家单击Enter按钮时等价于点击play button
    if not stats.game_state:
        # 初始化并开始游戏
        initialize_and_start_game(global_set, screen, stats, score_board, aliens, ship, bullets)


def check_play_button(global_set, screen, stats, score_board, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    #  在玩家单击 Play 按钮时开始新游戏
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        if not stats.game_state:
            # 初始化并开始游戏
            initialize_and_start_game(global_set, screen, stats, score_board, aliens, ship, bullets)


def check_events(global_set, screen, stats, score_board, play_button, ship, aliens, bullets, mouse_cursor):
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
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_cursor.update(mouse_x, mouse_y)


def update_screen(back_ground, mouse_cursor, stats, screen, score_board, ship, aliens, bullets, play_button, fires):
    #  更新屏幕上的图像，并切换到新屏幕
    #  每次循环时都重绘屏幕
    #  1、最底层  背景色
    # screen.fill(global_set.bg_color)
    back_ground.blitme()
    #  2、绘制外星人群
    aliens.draw(screen)
    #  3、在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #  4、绘制飞船
    ship.blitme()
    #  5 绘制爆炸效果
    for fire in fires.sprites():
        fire.blitme()
    #  fires.draw(screen)
    #  5、绘制分数栏
    screen.fill(score_board.score_bar_bg_color, score_board.score_bar_rect)
    #  6、显示得分
    score_board.show_score()
    #  7、如果游戏处于非活动状态，就绘制 Play 按钮
    if not stats.game_state:
        play_button.draw_button()
        mouse_cursor.blitme()
    #  让最近绘制的屏幕可见
    pygame.display.flip()
    #  pygame.display.update()


def check_high_score(stats, score_board):
    #  检查是否诞生了新的最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()


def sound_aliens(stats):
    audio = 'audio/pig' + str(stats.level % 10) + '.wav'
    sound = pygame.mixer.Sound(audio)
    sound.play()


def create_fire(collisions, bullets, fires):
    #  更新子弹的位置
    bullets.update()
    #  将碰撞子弹放入fires
    fires.add(collisions)


def check_bullet_alien_collisions(global_set, stats, screen, score_board, ship, aliens, bullets, fires):
    #  响应子弹和外星人的碰撞
    #  删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # 计算碰撞字典中碰撞个数并计算得分
        for liens in collisions.values():
            stats.score += global_set.alien_points * len(liens)
            if len(liens):
                sound_aliens(stats)
        #  创建火花状态
        create_fire(collisions, bullets, fires)
        #  更新计分牌
        score_board.prep_score()
        check_high_score(stats, score_board)
    #  检测游戏结束
    if len(aliens) == 0:
        if len(fires) == 0:
            start_new_level(global_set, screen, stats, score_board, ship, aliens, bullets)


def start_new_level(global_set, screen, stats, score_board, ship, aliens, bullets):
    # 提高等级
    stats.level += 1
    #  删除现有的所有子弹，并创建一个新的外星人群
    bullets.empty()
    global_set.increase_speed()
    create_fleet(global_set, screen, stats, score_board, ship, aliens)
    #  更新等级信息
    score_board.prep_level()
    #  更新游戏状态
    stats.game_state = 11
    #  播放开始音效
    play_read_go(global_set)


def update_bullets(global_set, stats, screen, score_board, ship, aliens, bullets, fires):
    #  更新子弹的位置
    bullets.update()
    #  删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= score_board.score_bar_height:
            bullets.remove(bullet)
    check_bullet_alien_collisions(global_set, stats, screen, score_board, ship, aliens, bullets, fires)


def fire_bullet(global_set, screen, ship, bullets):
    #  如果还没有到达限制，就发射一颗子弹
    #  创建一颗子弹，并将其加入到编组 bullets 中
    if len(bullets) < global_set.bullets_allowed:
        new_bullet = Bullet(global_set, screen, ship)
        new_bullet.suondme()
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


def create_alien(global_set, screen, stats, score_board, aliens, alien_number, row_number):
    #  创建一个外星人并将其放在当前行
    alien = Aliens(global_set, screen, stats)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = score_board.score_bar_height + alien.rect.height * 0.5 + 2 * alien.rect.height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)


def create_fleet(global_set, screen, stats, score_board, ship, aliens):
    #  创建外星人群
    #  创建一个外星人，并计算每行可容纳多少个外星人
    alien = Aliens(global_set, screen, stats)
    number_aliens_x = get_number_aliens_x(global_set, alien.rect.width)
    number_rows = get_number_rows(global_set, score_board, ship.rect.height, alien.rect.height)
    #  创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(global_set, screen, stats, score_board, aliens, alien_number, row_number)


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


def ship_hit(global_set, stats, score_board):
    #  响应被外星人撞到的飞船
    #  将 ships_left 减 1
    stats.ships_left -= 1
    #  更新游戏状态信息  坠机阶段
    stats.game_state = 3
    # 更新记分牌
    score_board.prep_ships()
    #  播放撞击声
    global_set.ship_hit_audio_channel = global_set.ship_hit_audio.play()
    global_set.ship_hit_audio.play()


def level_again_or_start_new_level(global_set, stats, screen, score_board, ship, aliens, bullets):
    #  处理子弹和飞船
    if stats.ships_left > 0:
        #  重开此level
        start_game(global_set, screen, stats, score_board, aliens, ship, bullets)
    else:
        game_over(stats)


def game_over(stats):
    #  更新游戏状态信息  坠机阶段
    stats.game_state = 0
    # 光标可见
    pygame.mouse.set_visible(True)


def check_aliens_bottom(screen, aliens):
    lose_ship_flag = False
    #  检查是否有外星人到达了屏幕底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #  标记为真
            lose_ship_flag = True
            break
    return lose_ship_flag


def update_aliens(global_set, stats, screen, score_board, ship, aliens):
    #  更新外星人群中所有外星人的位置
    #  检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    check_fleet_edges(global_set, aliens)
    aliens.update()
    lose_ship_flag = False
    #  检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        lose_ship_flag = True
    #  检查是否有外星人到达屏幕底端
    lose_ship_flag = check_aliens_bottom(screen, aliens)
    if lose_ship_flag:
        ship_hit(global_set, stats, score_board)


def update_fires(fires):
    #  更新火花
    for fire in fires.sprites():
        #  更新火花的序列编号
        fire.update_fire()
        #  删除已消失的子弹
        if fire.explode_index >= 7:
            fires.remove(fire)
