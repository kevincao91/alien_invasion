class Settings():
    # 配置游戏所有的设置数据
    def __init__(self):
        #  初始化游戏的设置
        #  屏幕设置
        self.screen_width = 500
        self.screen_height = 500
        self.bg_color = (230, 230, 230)
        self.game_title = "Alien Invasion"
        self.speed_factor = 0.5
        #  子弹设置
        self.bullet_speed_factor = 0.3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 60, 60
        self.bullets_allowed = 20
