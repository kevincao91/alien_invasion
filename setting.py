class Settings():
    # 配置游戏所有的设置数据
    def __init__(self):
        #  初始化游戏的静态设置

        #  屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #  标题设置
        self.game_title = "Alien Invasion"

        #  游戏信息存储文件路径设置
        self.info_file = "game_info.json"

        #  飞船设置
        self.ship_speed_factor = 1.5  # 后面有再初始化设置
        self.ship_limit = 3

        #  子弹设置
        self.bullet_speed_factor = 2  # 后面有再初始化设置
        self.bullet_width = 800
        self.bullet_height = 15
        self.bullet_color = 255, 60, 60
        self.bullets_allowed = 20

        #  外星人设置
        self.alien_high_fill_factor = 0.6
        self.alien_speed_factor = 1  # 后面有再初始化设置
        self.fleet_drop_speed = 20
        # fleet_direction 为 1 表示向右移，为 -1 表示向左移
        self.fleet_direction = 1  # 后面有再初始化设置

        # 初始击落外星人得分
        self.alien_points = 5     # 后面有再初始化设置

        # 外星人点数的提高速度
        self.score_scale = 1.5
        #  加快游戏节奏参数
        self.ship_speedup_scale = 1.2
        self.bullet_speedup_scale = 1.2
        self.alien_speedup_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #  初始化随游戏进行而变化的设置
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1
        self.alien_points = 5

    def increase_speed(self):
        #  提高速度设置
        self.ship_speed_factor *= self.ship_speedup_scale
        self.bullet_speed_factor *= self.bullet_speedup_scale
        self.alien_speed_factor *= self.alien_speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

