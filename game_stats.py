class GameStats():
    #  跟踪游戏的统计信息
    def __init__(self, global_set):
        #  初始化统计信息
        self.global_set = global_set
        self.ships_left = global_set.ship_limit
        #  让游戏一开始处于非活动状态
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        #  初始化在游戏运行期间可能变化的统计信息
        self.ships_left = self.global_set.ship_limit
