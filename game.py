import arcade

SCREEN_WIDTH = 800
SCREEN_HEITH = 600
SCREEN_TITLE = "Pong Game"

BRICK_IN_STRING = 7
BRICK_STRINGS_COUNT = 6


class Brick(arcade.Sprite):
    def __init__(self):
        super().__init__('brick.png', 0.9)
        self.get_adjusted_hit_box()

    #def update(self, other):
    #    if arcade.check_for_collision(self, other):

class BrickList(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.brick_sprite = Brick()

class Ball(arcade.Sprite):
    def __init__(self):
        super().__init__('ball.png', 0.8)
        self.change_x = 3
        self.change_y = 3
        self.get_adjusted_hit_box()

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right > SCREEN_WIDTH:
            self.change_x = - self.change_x
        if self.left <= 0:
            self.change_x = - self.change_x
        if self.top > SCREEN_HEITH:
            self.change_y = - self.change_y
        if self.bottom <= 0:
            self.change_y = - self.change_y


class Bar(arcade.Sprite):
    def __init__(self):
        super().__init__('bar.png', 2.0)
        

    def update(self):
        self.center_x += self.change_x
        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.left <= 0:
            self.left = 0


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.bar = Bar()
        self.ball = Ball()
        self.brick_list = BrickList()
        self.setup()

    def setup(self):
        self.bar.center_x = SCREEN_WIDTH / 2
        self.bar.center_y = SCREEN_HEITH / 5
        self.ball.center_x = SCREEN_WIDTH / 2
        self.ball.center_y = SCREEN_HEITH / 4

        brick_counter = 1
        string_counter = 1

        for i in range(BRICK_IN_STRING * BRICK_STRINGS_COUNT):
            brick = Brick()
            brick.center_x = brick_counter * (SCREEN_WIDTH // BRICK_IN_STRING) - 55
            brick.center_y = SCREEN_HEITH  - string_counter * (SCREEN_HEITH // (2 * BRICK_STRINGS_COUNT))
            self.brick_list.append(brick)

            brick_counter += 1
            if brick_counter > BRICK_IN_STRING:
                brick_counter = 1
                string_counter += 1

    def on_draw(self):
        arcade.start_render()
        self.clear((0, 0, 0))
        self.bar.draw()
        self.ball.draw()
        self.brick_list.draw()

    def update(self, delta):
        if arcade.check_for_collision(self.bar, self.ball):
            if self.ball.bottom > self.bar.bottom and self.ball.top < self.bar.top:
                if self.ball.change_x > 0 >= self.bar.change_x or self.ball.change_x < 0 <= self.bar.change_x:
                    self.ball.change_x = - self.ball.change_x
                elif self.ball.change_x > 0:
                    self.ball.change_x = self.bar.change_x + 1
                else:
                    self.ball.change_x = self.bar.change_x - 1
            else:
                self.ball.change_y = - self.ball.change_y

        for brick in self.brick_list:
            if arcade.check_for_collision(self.ball, brick):
                if self.ball.bottom >= brick.bottom and self.ball.top <= brick.top:
                    self.ball.change_x = - self.ball.change_x
                else:
                    self.ball.change_y = - self.ball.change_y

                brick.remove_from_sprite_lists()

        self.ball.update()
        self.bar.update()

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.RIGHT:
            self.bar.change_x = 6
        if key == arcade.key.LEFT:
            self.bar.change_x = -6

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.RIGHT:
            self.bar.change_x = 0
        if key == arcade.key.LEFT:
            self.bar.change_x = 0


if __name__ == '__main__':
    window = Game(SCREEN_WIDTH, SCREEN_HEITH, SCREEN_TITLE)
    arcade.run()
