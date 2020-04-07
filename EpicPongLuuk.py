import arcade
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CENTERSCREEN_X = SCREEN_WIDTH/2
CENTERSCREEN_Y = SCREEN_HEIGHT/2
SCREEN_TITLE = "Pong"

MOVEMENT_SPEED = 250

PADDLE_SPEED = 100
PADDLE_BOT_SPEED = 85
PADDLE_HUMAN_START_X = 15
PADDLE_BOT_START_X = SCREEN_WIDTH-15
SCOREYOU = 0
SCOREBOT = 0

STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2


COLORMODE = False
R = G = B = 250
COLORA = (R-250, G-250, B-250)
COLORB = (R, G, B)


class Ball:
    def __init__(self, position_x, position_y, change_x, change_y, radius, color):
        """ Take the parameters out of the Ball class, and create instance variables with the parameters. """
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color

    def draw(self):
        """ Tell to our Ball class how it should draw it. """
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self, player_a, player_b, delta_time):
        """ Tell to our Ball class how it should update it. """
        # Move the ball
        self.position_y += self.change_y * delta_time
        self.position_x += self.change_x * delta_time

        # Make the ball bounce of the bottom and top walls
        if self.position_y - self.radius <= 0 or self.position_y + self.radius >= SCREEN_HEIGHT:
            self.change_y = self.change_y * -1

        # See if the ball hits the paddle
        # TODO: Bereken het :)
        if self.position_x < 35 and (player_a.position_y+50) > self.position_y and (player_a.position_y-50) < self.position_y:
            self.change_x *= -1
        if self.position_x > SCREEN_WIDTH-35 and (player_b.position_y+50) > self.position_y and (player_b.position_y-50) < self.position_y:
            self.change_x *= -1

        # Also check if the ball hits the edge of the paddle
        # if self.position_x <= 35 and self.position_x >= 0 and (player_a.position_y-50) > self.position_y or (player_a.position_y+50) < self.position_y:
        #    self.change_x *= -1

        # if self.position_x > SCREEN_WIDTH-35 and (player_b.position_y+50) > self.position_y and (player_b.position_y-50) < self.position_y:
        #    self.change_x *= -1


class Paddle:
    def __init__(self, position_x, position_y, change_x, change_y, width, height, color, humanorbot, name):
        """ Take the parameters out of the Paddle class, and create instance variables with the parameters. """
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.width = width
        self.height = height
        self.color = color
        self.humanorbot = humanorbot
        self.name = name

    def draw(self):
        """ Tell to our Paddle class how it should draw the paddle. """
        arcade.draw_rectangle_filled(self.position_x, self.position_y, self.width, self.height, self.color)

    def update(self, ball, delta_time):
        """ Tell to our Paddle class how it should update it. """
        # Move the paddle

        self.position_y += self.change_y * delta_time
        self.position_x += self.change_x * delta_time

        # See if the paddle hits the edge of the screen. If so, stop the paddle.
        if self.position_y < self.height/2:
            self.position_y = self.height/2
        if self.position_y > SCREEN_HEIGHT - self.height/2:
            self.position_y = SCREEN_HEIGHT - self.height/2

        # A small system that will see if the paddle is a human or a bot and if so what controls should it use.
        if self.humanorbot == "human":
            # print(self.name)
            pass
        if self.humanorbot == "bot":
            # print(self.name)
            if self.position_y < ball.position_y:
                self.position_y += PADDLE_BOT_SPEED * delta_time
            if self.position_y > ball.position_y:
                self.position_y -= PADDLE_BOT_SPEED * delta_time


class Points:
    def __init__(self, scoreb, scorey, scorey_x, scorey_y, scoreb_x, scoreb_y, color):
        """ Take the parameters out of the Points class, and create instance variables with the parameters. """
        self.scoreb = scoreb
        self.scorey = scorey
        self.scorey_x = scorey_x
        self.scorey_y = scorey_y
        self.scoreb_x = scoreb_x
        self.scoreb_y = scoreb_y
        self.color = color

    def update(self, ball, bot, gamestate):
        """ Tell to our Points class how it should update it. """
        # Add points to the bot if the bot scores
        if ball.position_x < 15:
            self.scoreb += 1
            ball.position_x = SCREEN_WIDTH/2
            ball.position_y = SCREEN_HEIGHT/2
            bot.position_y = SCREEN_HEIGHT/2

        # Add points to the player if the player scores
        if ball.position_x > SCREEN_WIDTH-15:
            self.scorey += 1
            ball.position_x = SCREEN_WIDTH/2
            ball.position_y = SCREEN_HEIGHT/2
            bot.position_y = SCREEN_HEIGHT/2

        if self.scoreb >= 3 or self.scorey >= 3:
            self.gamestate = STATE_GAME_OVER
            ball.position_x = CENTERSCREEN_X
            ball.position_y = 20

    def draw(self, scoreb, scorey, scorey_x, scorey_y, scoreb_x, scoreb_y):
        """ Tell to our Points class how it should draw it. """
        arcade.draw_point(scorey_x, scorey_y, self.color, 0)
        arcade.draw_text(f"{self.scorey}", self.scorey_x, self.scorey_y, self.color, 32, width=200, align="center", anchor_x="center", anchor_y="center")

        arcade.draw_point(scoreb_x, scoreb_y, self.color, 0)
        arcade.draw_text(f"{self.scoreb}", self.scoreb_x, self.scoreb_y, self.color, 32, width=200, align="center", anchor_x="center", anchor_y="center")

        if self.scoreb >= 3:
            arcade.draw_point(CENTERSCREEN_X, CENTERSCREEN_Y, self.color, 0)
            arcade.draw_text(f"THE BOT WON!\nPress the space bar \nto play again", CENTERSCREEN_X, CENTERSCREEN_Y-20,
                             self.color, 32, width=500, align="center", anchor_x="center", anchor_y="center")
        if self.scorey >= 3:
            arcade.draw_point(CENTERSCREEN_X, CENTERSCREEN_Y, self.color, 0)
            arcade.draw_text(f"YOU WON!\nPress the space bar \nto play again", CENTERSCREEN_X, CENTERSCREEN_Y-20,
                             self.color, 32, width=500, align="center", anchor_x="center", anchor_y="center")


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        # Call the parent class's init function to draw the window (standard OOP stuff)
        super().__init__(width, height, title)
        arcade.set_background_color(COLORA)

        """ Give the classes inits there parameters. """
        self.ball = Ball(CENTERSCREEN_X, CENTERSCREEN_Y, MOVEMENT_SPEED, MOVEMENT_SPEED, 15, COLORB)
        self.player_a = Paddle(PADDLE_HUMAN_START_X, CENTERSCREEN_Y, 0, 0, 15, 100, COLORB, "human", "player_a")
        self.player_b = Paddle(PADDLE_BOT_START_X, CENTERSCREEN_Y, 0, 0, 15, 100, COLORB, "bot", "player_b")
        self.points = Points(SCOREBOT, SCOREYOU, SCREEN_WIDTH/3, SCREEN_HEIGHT-15, (SCREEN_WIDTH/3)*2, SCREEN_HEIGHT-15, COLORB)
        self.color_mode = COLORMODE

        """ Some local variables """
        self.game_state = 0  # menu
        self.game_state = 1  # playing
        self.game_state = 2  # game over

    def on_setup(self):
        self.game_state = STATE_MENU

    def on_draw(self):
        """ Called whenever we need to draw the window, and draw the classes. """
        arcade.start_render()
        self.ball.draw()
        self.player_a.draw()
        self.player_b.draw()
        self.points.draw(SCOREBOT, SCOREYOU, SCREEN_HEIGHT-15, SCREEN_WIDTH/3, SCREEN_HEIGHT-15, (SCREEN_WIDTH/3)*2)

    def on_update(self, delta_time):
        """ Update every class every. """
        if self.game_state == STATE_MENU:
            pass

        elif self.game_state == STATE_PLAYING:
            self.ball.update(self.player_a, self.player_b, delta_time)
            self.player_a.update(self.ball, delta_time)
            self.player_b.update(self.ball, delta_time)
            self.points.update(self.ball, self.player_b, self.game_state)
            # Cool color mode thing
            if self.color_mode:
                r = random.randrange(1, 255)
                g = random.randrange(1, 255)
                b = random.randrange(1, 255)
                color = (g, b, r)
                colorb = (r, g, b)
                arcade.set_background_color(color)
            elif self.color_mode == False:
                r = g = b = 250
                color = (r-250, g-250, b-250)
                colorb = (r, g, b)
                arcade.set_background_color(color)
            self.player_a.color = colorb
            self.player_b.color = colorb
            self.ball.color = colorb
        elif self.game_state == STATE_GAME_OVER:
            pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.UP:
            self.player_a.change_y = PADDLE_SPEED
        elif key == arcade.key.DOWN:
            self.player_a.change_y = -PADDLE_SPEED

        elif key == arcade.key.C:
            self.color_mode = not self.color_mode

        elif key == arcade.key.SPACE:
            if self.game_state != 1:
                self.game_state = 1
                SCOREYOU = 0
                SCOREBOT = 0

    def on_key_release(self, key, modifiers):
        """ Called whenever the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_a.change_y = 0


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
