import time

import arcade

WIDTH = 800
HEIGHT = 600
GRAVITY = 0.6
EXITPOS = 10300
SHIFT_DURATION = 5
SHIFT_COOLDOWN = 15
ZOMBI_SPEED = 1.3
LAYER_NAME_PLAYER = "Player"


class Zombie(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:/images/animated_characters/zombie/zombie_idle.png",center_x=x, center_y=y)
    def update(self, delta_time: float = 1 / 60):
        super().update()


class LoseView1(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.bggame1 = arcade.load_texture('defeat.png')
        window.set_viewport(0, WIDTH, 0, HEIGHT)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(texture=self.bggame1, width=WIDTH, height=HEIGHT, center_x=WIDTH / 2,
                                      center_y=HEIGHT / 2)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        game = Game()
        window.show_view(game)
class WinView1(arcade.View):
    def __init__(self):
        global star1
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        gameView = WindowGame1()
        self.bggame1 = arcade.load_texture('victory.png')
        window.set_viewport(0, WIDTH, 0, HEIGHT)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(texture=self.bggame1, width=WIDTH, height=HEIGHT, center_x=WIDTH / 2,
                                      center_y=HEIGHT / 2)
# Класс игрока
class Player(arcade.AnimatedTimeBasedSprite):
    def __init__(self):
        super().__init__(":resources:/images/animated_characters/male_person/malePerson_idle.png", center_y=328, center_x=-100)
        self.jump_speed = 12
        self.on_ground = False
        self.player_speed = 4
        self.immortality_time = 2
        self.goRight = False
        self.goLeft = False

    # Обновление игрока
    def update(self):
        super().update()

# Класс окна
class Game(arcade.View):
    def __init__(self):
        global diff
        super().__init__()
        arcade.set_background_color(arcade.color.BUFF)
        self.game_over = False
        self.score = 0
        self.scene = arcade.Scene()
        self.cef = 1
        self.live = 3
        self.zombi_vision = 400

        # Все что связанно с жизнями
        self.lives_smesh = 0
        self.collision = False

        self.heart = arcade.load_texture(":resources:/images/tiles/stone.png")
        self.live_used = False

        # Создание игрока
        self.scene.add_sprite_list('Player')
        self.player = Player()
        self.scene.add_sprite('Player', self.player)

        # Все что связанно с ускорением
        self.shift_was_used = False
        self.Shift = False
        self.CoolDown = False

        self.time_texture_load = 0.2
        self.texture_num = 0
        # Объекты
        self.obstacles = ['Spikes', 'Zombie', 'Cactus']  #список препятствий
        self.listSpikes = [[400,128], [1400,128], [3000,128], [5600,128], [1756,128], [1884,128],[2012, 128],[2140,128],
                           [7000, 128], [7256, 128], [7384, 128], [7512, 128], [7640, 128], [7768, 128], [7896, 128],           #координаты шипов
                           [8024, 128], [8152, 128], [8280, 128], [8408, 128], [8536, 128], [8664, 128], [8792, 128], [8920, 128], [4200, 128],
                           [9048, 128], [9176, 128], [9304, 128], [9432, 128], [9560, 128], [9688, 128], [9816, 128]
                           ]
        self.listZombie = [[1100,128],[4000,128], [5900,128], [4630,128]]   # координаты зомби
        self.listCactus = [[760,128], [2610,128],[3550, 128], [6270,128], [6370,128], [5150,128]]    #координаты  кактусов

        self.listPlatform = [[1690,180,'grassHalf'],[1850,300,'grassHalf'], [2078, 200, 'grassHalf'], [7300,220, 'snowHalf'],
                             [7100,400,'snowHalf'], [7400,500,'snowHalf'], [7700,300,'snowHalf'], [7900,400,'snowHalf'],
                             [8100,300,'snowHalf'],[7300,1200,'snowHalf'],[7100,1300,'snowHalf'], [8400, 500, 'snowHalf'],
                             [8650,650, 'snowHalf'],[8400,900, 'snowHalf'], [8600, 1100, 'snowHalf'],[8900, 1100, 'snowHalf'],
                             [9250, 1000, 'snowHalf'],[9500, 800, 'snowHalf'],[9700, 340, 'snowHalf'],[10000,340, 'snowHalf']
                             ]# координаты платформ
        self.listMoney = [[580,278] ,[1850,478], [2790, 278], [4150,278], [5375,278], [7100,700], [8400,1200], [7900,600], [9300,1300]]       # координаты монет
        self.listLadder = [[7500,825], [7500,864],[7500,928],[7500,992],[7500,1058],[7500,1120],[7500,1184],[9700,800],[9700,736],[9700,672],
                           [9700,604],[9700,544], [9700,480]]
        self.listHeart = [[5900, 300], [7000,1600]]



        #  Создание пола и стен и платформ
        self.scene.add_sprite_list('Grass')
        for x in range(-300, 10500, 64):
            grass = arcade.Sprite(":resources:/images/tiles/grassMid.png", center_y=32, center_x=x,scale=0.5)
            self.scene.add_sprite('Grass', grass)
        for x in range(-332, 10500, 10831):
            for y in range(90,  390, 64):
                wall = arcade.Sprite(":resources:/images/tiles/grassMid.png", center_y=y, center_x=x, scale=0.5)
                self.scene.add_sprite('Grass', wall)
        self.scene.add_sprite_list('Snow')
        for x in range(6504, 10500,64):
            snow_grass = arcade.Sprite(":resources:/images/tiles/snowMid.png", center_x=x, center_y=32, scale=0.5)
            snow = arcade.Sprite(":resources:/images/tiles/snow_pile.png", center_x=x, center_y=128)
            self.scene.add_sprite('Snow', snow)
            self.scene.add_sprite('Grass', snow_grass)
        for y in range(128,326,64):
            wall = arcade.Sprite(":resources:/images/tiles/brickGrey.png", center_y=y, center_x=9600)
            self.scene.add_sprite('Grass', wall)


        for i in self.listPlatform:
            platform = arcade.Sprite(f":resources:/images/tiles/{i[2]}.png", center_x=i[0],
                                   center_y=i[1], scale=0.5)
            self.scene.add_sprite('Grass', platform)

        # создание дополнительного сердца на карте
        self.scene.add_sprite_list('LifePlus')
        for i in self.listHeart:
            serdce = arcade.Sprite(":resources:/images/tiles/stone.png", center_x=i[0], center_y=i[1], scale=0.4)
            self.scene.add_sprite('LifePlus', serdce)

        #  Создание шипов
        self.scene.add_sprite_list('Spikes')
        for i in self.listSpikes:
            spikes = arcade.Sprite(":resources:/images/tiles/spikes.png", center_x=i[0], center_y=i[1], scale=1)
            self.scene.add_sprite('Spikes', spikes)

        self.scene.add_sprite_list('Ladders')
        for i in self.listLadder:
            ladder = arcade.Sprite(":resources:/images/tiles/ladderMid.png", center_x=i[0], center_y=i[1], scale=0.5)
            self.scene.add_sprite('Ladders', ladder)

        #  Создание кактусов
        self.scene.add_sprite_list('Cactus')
        for i in self.listCactus:
            cactus = arcade.Sprite(":resources:/images/tiles/cactus.png", center_x=i[0],
                                   center_y=i[1])
            self.scene.add_sprite('Cactus', cactus)

        #  Создание зомби
        self.scene.add_sprite_list('Zombie')
        for i in self.listZombie:
            zombie = Zombie(i[0], i[1])
            self.scene.add_sprite('Zombie', zombie)

        #  Создание монет
        self.scene.add_sprite_list('Money')
        for i in self.listMoney:
            money = arcade.Sprite(":resources:/images/items/coinGold.png", center_x=i[0], center_y=i[1], scale=0.5)
            self.scene.add_sprite('Money', money)


        #  Создание выхода
        self.exit = arcade.Sprite(":resources:/images/tiles/signExit.png", center_x=EXITPOS, center_y=100, scale= 0.6)
        self.scene.add_sprite('exit', self.exit)


        #  Движок
        self.engine = arcade.PhysicsEnginePlatformer(self.player, self.scene.get_sprite_list('Grass'),
                                                     gravity_constant=GRAVITY, ladders=self.scene.get_sprite_list('Ladders'))

        #  Камера
        self.camera = arcade.Camera(self.window.width, self.window.height)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.camera.use()


        # Отрисовка сердец, скорости, координат
        for i in range(1, self.live+1):
            arcade.draw_texture_rectangle(center_x=self.player.center_x-34+i*17-self.lives_smesh,
                                          center_y=self.player.center_y+40, width=20,height=20,texture=self.heart)
            arcade.draw_text(f'x={round(self.player.center_x)}\n y={round(self.player.center_y)} \n speed {self.player.player_speed} px/un',
                             self.player.center_x-WIDTH/2+20, self.player.center_y-100, arcade.color.BLACK, font_size=9)
            try:
                if SHIFT_COOLDOWN - round(time.time() - self.time_on_shift) >= 0:
                    arcade.draw_text(
                        f'\n shift cooldown { SHIFT_COOLDOWN - round(time.time() - self.time_on_shift)}s  `score {self.score}`',
                        self.player.center_x-WIDTH/2+20, self.player.center_y - 120, arcade.color.BLACK, font_size=9)
                else:
                    arcade.draw_text(
                        f'\n shift cooldown 0s  score {self.score}',
                        self.player.center_x-WIDTH/2+20, self.player.center_y - 120, arcade.color.BLACK, font_size=9)
                    self.shift_was_used = False
            except:
                arcade.draw_text(
                    f'\n shift cooldown 0s  score {self.score}',
                    self.player.center_x-WIDTH/2+20, self.player.center_y - 120, arcade.color.BLACK, font_size=9)


    def on_update(self, delta_time: 1/20):
        self.on_draw()
        self.scene.update()
        self.engine.update()

        if time.time()-self.time_texture_load >= 0.05:
            if self.engine.can_jump():
                self.texture_num += 1
                if self.texture_num <= 7 :
                    if self.player.goLeft:

                        self.player.texture = arcade.load_texture(
                                f":resources:/images/animated_characters/male_person/malePerson_walk{self.texture_num}.png",flipped_horizontally=True)
                        self.time_texture_load = time.time()

                    elif self.player.goRight:
                        self.player.texture = arcade.load_texture(
                            f":resources:/images/animated_characters/male_person/malePerson_walk{self.texture_num}.png")
                        self.time_texture_load = time.time()
                    else:
                        self.player.texture = arcade.load_texture(":resources:/images/animated_characters/male_person/malePerson_idle.png")
                else:
                    self.texture_num = 0
            else:
                self.player.texture = arcade.load_texture(
                    ":resources:/images/animated_characters/male_person/malePerson_fall.png")
        # перемещение камеры
        if self.game_over == False:
            self.center_camera_to_player()

        # проверка шифта
        try:
            if time.time() - self.time_on_shift >= SHIFT_DURATION:
                if self.CoolDown == True:
                    self.player.player_speed = 4

                self.Shift = False
                if time.time() - self.time_on_shift >= SHIFT_COOLDOWN:
                    self.CoolDown = False
                    self.Shift = False
                    self.shift_was_used = True
        except:
            pass

        # логика зомби
        for i in self.scene.get_sprite_list('Zombie'):
            if i.center_x - self.player.center_x <= self.zombi_vision and  i.center_x - self.player.center_x >= 0:
                i.change_x = -ZOMBI_SPEED*self.cef
            if i.center_x - self.player.center_x >= self.zombi_vision:
                i.change_x = 0
            if self.player.center_x - i.center_x <= self.zombi_vision and self.player.center_x - i.center_x >= 0:
                i.change_x = ZOMBI_SPEED*self.cef
            if self.player.center_x - i.center_x >= self.zombi_vision:
                i.change_x = 0



        # если поймал монету
        for i in self.scene.get_sprite_list('Money'):
            if arcade.check_for_collision(self.player, i):
                 i.kill()
                 self.score += 1

        # уменьшение жизней если столкнулся с чемто, конец игры
        for i in self.obstacles:
            if arcade.check_for_collision_with_list(self.player, self.scene.get_sprite_list(i)):
                if self.collision == False:
                    self.live -= 1
                    self.collision = True
                    if self.live <= 0:
                        self.player.kill()
                        lose = LoseView1()
                        window.show_view(lose)

                    self.time_now = time.time()
            try:
                if time.time() - self.time_now >= self.player.immortality_time:
                    self.collision = False
            except:
                pass




        # колизия с выходом
        if arcade.check_for_collision(self.player, self.exit):
            self.game_over = True
            win = WinView1()
            window.show_view(win)

        # колизия с сердцами
        for i in self.scene.get_sprite_list('LifePlus'):
            if arcade.check_for_collision(self.player, i) and self.live_used == False:
                self.live_used = True
                self.live += 1
                i.kill()

    # перемещение камеры логика
    def center_camera_to_player(self):
        center_x = self.player.center_x - self.camera.viewport_width / 2
        center_y = self.player.center_y - self.camera.viewport_height / 2
        if center_y < 0:
            center_y = 0
        self.camera.move_to((center_x, center_y))

    #  Обработка нажатий
    def on_key_press(self, symbol: int, modifiers: int):
        if (symbol == arcade.key.UP or symbol == arcade.key.W or symbol == arcade.key.SPACE) and self.engine.can_jump():
            if self.engine.can_jump():
                self.player.change_y = self.player.jump_speed
                self.player.on_ground = False
        if symbol == arcade.key.LEFT or symbol == arcade.key.A :
            self.player.goLeft = True
            self.player.change_x -= self.player.player_speed
            self.lives_smesh = 10
            self.live_used = False
        if symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.goRight = True
            self.player.change_x += self.player.player_speed
            self.lives_smesh = -10
            self.live_used = False

        # ускорение
        if symbol == arcade.key.LSHIFT:
            self.Shift = not self.Shift
            if not self.Shift and self.shift_was_used == True:
                try:
                    if time.time() - self.time_on_shift >= SHIFT_DURATION:
                        if self.CoolDown == True:
                            self.player.player_speed = 4
                        self.Shift = False
                        if time.time() - self.time_on_shift >= SHIFT_COOLDOWN:
                            self.CoolDown = False
                            self.Shift = False
                            self.shift_was_used = False
                except:
                    pass
            self.shift_was_used = False
            if self.shift_was_used == False:
                self.time_on_shift = time.time()

            if self.Shift == True and self.CoolDown == False:
                self.CoolDown = True
                self.player.player_speed = 6
                self.shift_was_used = True

            else:
                self.player.player_speed = 4





    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player.change_y = 0

        if symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x = 0
            self.player.goLeft = False
            self.lives_smesh = 0
        if symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.goRight = False
            self.player.change_x = 0
            self.lives_smesh = 0



if __name__ == '__main__':
    window = arcade.Window(WIDTH, HEIGHT, resizable=True)
    game = Game()
    window.show_view(game)
    window.run()
