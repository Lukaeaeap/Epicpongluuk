import arcade
import random
from termcolor import colored

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CENTERSCREEN_X = SCREEN_WIDTH/2
CENTERSCREEN_Y = SCREEN_HEIGHT/2
SCREEN_TITLE = "Pong"

MOVEMENT_SPEED = 150

PADDLE_SPEED = 200
PADDLE_BOT_SPEED = 200
PADDLE_HUMAN_START_X = 15
PADDLE_BOT_START_X = SCREEN_WIDTH-15
PADDLEWITH = 20
PADDLEHEIGHT = 100
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
    def __init__(self, position_x, position_y, change_x, change_y, radius, color, sound):
        """ Take the parameters out of the Ball class, and create instance variables with the parameters. """
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color
        self.sound = sound

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
            self.sound.play(volume=0.1)

        # See if the ball hits the paddle
        # TODO: Bereken het :)
        if self.position_x < player_a.position_x+PADDLEWITH and (player_a.position_y+50) > self.position_y and (player_a.position_y-50) < self.position_y:
            self.change_x = MOVEMENT_SPEED
            self.sound.play(volume=0.1)

        if self.position_x > SCREEN_WIDTH-35 and (player_b.position_y+50) > self.position_y and (player_b.position_y-50) < self.position_y:
            self.change_x = -MOVEMENT_SPEED
            self.sound.play(volume=0.1)





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
    def __init__(self, scoreb, scorey, scorey_x, scorey_y, scoreb_x, scoreb_y, color, sound):
        """ Take the parameters out of the Points class, and create instance variables with the parameters. """
        self.scoreb = scoreb
        self.scorey = scorey
        self.scorey_x = scorey_x
        self.scorey_y = scorey_y
        self.scoreb_x = scoreb_x
        self.scoreb_y = scoreb_y
        self.color = color
        self.Spacebar = arcade.Sprite("Pongsprites/Spacebar.png", scale=0.6, center_x=CENTERSCREEN_X, center_y=CENTERSCREEN_Y-100)
        self.sound = sound

    def update(self, ball, bot, gamestate):
        """ Tell to our Points class how it should update it. """
        # Add points to the bot if the bot scores
        if ball.position_x < 15:
            self.scoreb += 1
            ball.position_x = SCREEN_WIDTH/2
            ball.position_y = SCREEN_HEIGHT/2
            bot.position_y = SCREEN_HEIGHT/2
            self.sound.play(volume=0.1)

        # Add points to the player if the player scores
        if ball.position_x > SCREEN_WIDTH-15:
            self.scorey += 1
            ball.position_x = SCREEN_WIDTH/2
            ball.position_y = SCREEN_HEIGHT/2
            bot.position_y = SCREEN_HEIGHT/2
            self.sound.play(volume=0.1)

        if self.scoreb >= 3 or self.scorey >= 3:
            ball.position_x = SCREEN_WIDTH + 30
            ball.position_y = CENTERSCREEN_Y
            # print(self.gamestate)
        if gamestate == STATE_MENU:
            ball.position_x = SCREEN_WIDTH + 30
            ball.position_y = CENTERSCREEN_Y

    def draw(self, scoreb, scorey, scorey_x, scorey_y, scoreb_x, scoreb_y, gamestate, name):
        """ Tell to our Points class how it should draw it. """
        arcade.draw_point(scorey_x, scorey_y, self.color, 0)
        arcade.draw_text(f"{self.scorey}", self.scorey_x, self.scorey_y, self.color, 32, width=200, align="center", anchor_x="center", anchor_y="center")

        arcade.draw_point(scoreb_x, scoreb_y, self.color, 0)
        arcade.draw_text(f"{self.scoreb}", self.scoreb_x, self.scoreb_y, self.color, 32, width=200, align="center", anchor_x="center", anchor_y="center")

        # if the game is over print who won
        if gamestate == STATE_GAME_OVER:
            if self.scoreb >= 3:
                arcade.draw_point(CENTERSCREEN_X, CENTERSCREEN_Y, self.color, 0)
                arcade.draw_text("THE BOT WON!", CENTERSCREEN_X, CENTERSCREEN_Y-20,
                                 self.color, 32, width=500, align="center", anchor_x="center", anchor_y="center")

            if self.scorey >= 3:
                arcade.draw_point(CENTERSCREEN_X, CENTERSCREEN_Y, self.color, 0)
                arcade.draw_text("YOU WON!", CENTERSCREEN_X, CENTERSCREEN_Y-20,
                                 self.color, 32, width=500, align="center", anchor_x="center", anchor_y="center")

        if gamestate == STATE_MENU:
            arcade.draw_point(CENTERSCREEN_X, CENTERSCREEN_Y, self.color, 0)
            arcade.draw_text(f"Welcome, {name}\n EpicPong by Luuk\n", CENTERSCREEN_X, CENTERSCREEN_Y+120,
                             arcade.color.BLUE, 32, width=500, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text("Press the space bar \nto start the game", CENTERSCREEN_X, CENTERSCREEN_Y+75,
                             self.color, 32, width=500, align="center", anchor_x="center", anchor_y="center")
            arcade.draw_text("WARNING: loud sounds", CENTERSCREEN_X, CENTERSCREEN_Y,
                             arcade.color.RED, 32, width=500, align="center", anchor_x="center", anchor_y="center")
            self.Spacebar.draw()


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        # Call the parent class's init function to draw the window (standard OOP stuff)
        super().__init__(width, height, title)
        arcade.set_background_color(COLORA)

        # give all variables a none variable if we want to start giving them value in on_setup
        self.ball = None

        self.player_a = None
        self.player_b = None

        self.points = None

        self.color_mode = None

        self.game_state = None
        self.total_time = None
        self.yourname = None

        self.sound1 = arcade.Sound("Pongsprites/Pongbliep.wav")
        self.sound2 = arcade.Sound("Pongsprites/Pongbliep2.wav")

    def on_setup(self):
        """ Give the classes inits there parameters. """
        self.yourname = input("Please enter your name: ")
        for i in range(20):
            if i == 1:
                print(colored(f'The game is starting, {self.yourname}', 'red', attrs=['bold']))
            if i == 15:
                print(colored('The game is made by Luuk Hoekstra\nCredits to: Cas, Kuno and Lex for helping with the coding\nMade with the python arcade, random and tempcolor libraries\nPress c for colormode\nPress space to start\nUse the up and down keys to move your paddle\nGood luck!', 'cyan', attrs=['bold']))

        self.color_mode = COLORMODE
        COLORB = arcade.color.WHITE

        self.game_state = STATE_MENU

        self.total_time = 4.0

        self.ball = Ball(CENTERSCREEN_X, CENTERSCREEN_Y, MOVEMENT_SPEED, MOVEMENT_SPEED, 15, COLORB, self.sound2)

        self.player_a = Paddle(PADDLE_HUMAN_START_X, CENTERSCREEN_Y, 0, 0, PADDLEWITH, 100, COLORB, "human", "player_a")
        self.player_b = Paddle(PADDLE_BOT_START_X, CENTERSCREEN_Y, 0, 0, PADDLEWITH, 100, COLORB, "bot", "player_b")

        self.points = Points(SCOREBOT, SCOREYOU, SCREEN_WIDTH/3, SCREEN_HEIGHT-15, (SCREEN_WIDTH/3)*2, SCREEN_HEIGHT-15, COLORB, self.sound1)

    def on_draw(self):
        """ Called whenever we need to draw the window, and draw the classes. """
        arcade.start_render()
        self.points.draw(SCOREBOT, SCOREYOU, SCREEN_HEIGHT-15, SCREEN_WIDTH/3, SCREEN_HEIGHT-15, (SCREEN_WIDTH/3)*2, self.game_state, self.yourname)
        if self.game_state == STATE_PLAYING:
            self.player_a.draw()
            self.player_b.draw()
            self.ball.draw()

        # Stuff for the game over timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        output = f"Time before new game starts:\n {minutes:02d}:{seconds:02d}"
        if self.game_state == STATE_GAME_OVER:
            arcade.draw_text(output, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 75, arcade.color.WHITE, 10, width=500, align="center", anchor_x="center", anchor_y="center")

    def on_update(self, delta_time):
        """ Update every class every. """
        if self.game_state == STATE_MENU:
            pass

        # Update for the playing game state
        elif self.game_state == STATE_PLAYING:
            self.ball.update(self.player_a, self.player_b, delta_time)

            self.player_a.update(self.ball, delta_time)
            self.player_b.update(self.ball, delta_time)

            # Check if the game should end
            self.points.update(self.ball, self.player_b, self.game_state)
            if self.points.scoreb >= 3 or self.points.scorey >= 3:
                self.game_state = STATE_GAME_OVER

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

        # Update for gameover, which makes a timer to automaticly go to the menu screen after 4 seconds
        elif self.game_state == STATE_GAME_OVER:
            self.total_time -= delta_time
            if self.total_time <= 0.0:
                print(colored('Restarting...', 'red', attrs=['bold']))
                self.total_time = 0.0
                self.on_setup()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. First we see if the game is running then we check which key is pressed and then our code."""
        if self.game_state == STATE_PLAYING:
            if key == arcade.key.UP:
                self.player_a.change_y = PADDLE_SPEED
            elif key == arcade.key.DOWN:
                self.player_a.change_y = -PADDLE_SPEED
            elif key == arcade.key.C:
                self.color_mode = not self.color_mode

        elif self.game_state == STATE_MENU:
            if key == arcade.key.SPACE:
                self.game_state = STATE_PLAYING
                self.sound1.play(volume=0.1)
        """
        elif self.game_state == STATE_GAME_OVER:
            if key == arcade.key.SPACE:
                self.on_setup()
        """

    def on_key_release(self, key, modifiers):
        """ Called whenever the user releases a key. We cant always move the paddle"""
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_a.change_y = 0


# Standard OOP stuff


def main():
    # Just for fun to get all of the requirements for the game.
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.on_setup()
    arcade.run()


if __name__ == "__main__":
    main()
