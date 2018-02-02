import json


class GameStats():
    #  跟踪游戏的统计信息
    def __init__(self, global_set):
        #  初始化统计信息
        self.global_set = global_set
        self.ships_left = global_set.ship_limit
        self.score = 0
        self.level = 1
        #  初始化游戏状态标记
        self.aliens_bullet_freeze_flag = True
        self.ship_freeze_flag = True
        self.is_boss = False
        self.boss_HP = 0
        # 在任何情况下都不应重置最高得分
        self.high_score = 0
        #  让游戏一开始处于非活动状态
        self.reset_stats()
        self.get_high_score()
        #  游戏state信息
        self.game_state = 0
        #  game_state值      游戏状态    飞船状态    外星人状态   子弹状态    对应阶段
        #  0                非激活状态   不可移动    不移动       不能产生  游戏未开始阶段
        #  1                激活状态     不可移动    不移动       不能产生  准备开始阶段
        #  2                激活状态      可移动      移动         能产生   正常游戏阶段
        #  3                激活状态     不可移动    不移动       不能产生     坠机阶段

    def reset_stats(self):
        #  初始化在游戏运行期间可能变化的统计信息
        self.ships_left = self.global_set.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        try:
            with open(self.global_set.info_file) as fileobject:
                self.high_score = json.load(fileobject)
        except FileNotFoundError:
            with open(self.global_set.info_file, 'w') as fileobject:
                json.dump(self.high_score, fileobject)
