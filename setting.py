class Settings():
    # 配置游戏所有的设置数据
    def __init__(self):
        #  初始化游戏的设置
        #  屏幕设置
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.game_title = "Alien Invasion"
        #  飞船设置
        self.ship_speed_factor = 2
        self.ship_limit = 3
        #  子弹设置
        self.bullet_speed_factor = 2
        self.bullet_width = 200
        self.bullet_height = 15
        self.bullet_color = 255, 60, 60
        self.bullets_allowed = 20
        #  外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 100
        # fleet_direction 为 1 表示向右移，为 -1 表示向左移
        self.fleet_direction = 1


