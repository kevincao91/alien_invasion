import sys
import pygame
from bullet import Bullet


def check_keydown_events(event, screen, global_set, little_cute, bullets):
    # 响应按键
    if event.key == pygame.K_RIGHT:
        little_cute.moving_right = True
    elif event.key == pygame.K_LEFT:
        little_cute.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(global_set, screen, little_cute, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, little_cute):
    #  响应松开
    if event.key == pygame.K_RIGHT:
        little_cute.moving_right = False
    elif event.key == pygame.K_LEFT:
        little_cute.moving_left = False


def check_events(screen, global_set, little_cute, bullets):
    # 响应按键和鼠标事件 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, screen, global_set, little_cute, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, little_cute)


def update_screen(global_set, screen, little_cute, bullets):
    #  更新屏幕上的图像，并切换到新屏幕
    #  每次循环时都重绘屏幕
    screen.fill(global_set.bg_color)
    little_cute.blitme()
    #  在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #  让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    #  更新子弹的位置
    bullets.update()
    #  删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(global_set, screen, little_cute, bullets):
    #  如果还没有到达限制，就发射一颗子弹
    #  创建一颗子弹，并将其加入到编组 bullets 中
    if len(bullets) < global_set.bullets_allowed:
        new_bullet = Bullet(global_set, screen, little_cute)
        bullets.add(new_bullet)