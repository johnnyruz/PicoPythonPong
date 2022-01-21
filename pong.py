import time
import picodisplay as display

CHAR_HEIGHT = 6
CHAR_WIDTH = 5

class Ball:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen

class Paddle:
    def __init__(self, x, y, h, w, pen):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.pen = pen

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GameState():
   Startup = 1
   Menu = 2
   Playing = 3

# Game State Variables
game_state = GameState.Startup
multiplayer = False

# Game Configuration Variables
paddle_width = 5
paddle_height = 30
paddle_move_speed = 2
ball_size = 5
ball_speed = 3
hitCount = 0

# Game Objects
balls = []
paddle1 = None
paddle2 = None

# Initialize Display
screen_width = display.get_width()
screen_height = display.get_height()
display_buffer = bytearray(screen_width * screen_height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)
display.set_backlight(1.0)

# Fills the screen with Black to clear it
def clear_display():
    display.set_pen(0,0,0)
    display.clear()

# Determines the starting point required to center text drawn by display.text()
def center_text(text: str, scale: int, screenWidth: int, screenHeight: int) :
    xPos = (screenWidth / 2) - (len(text) / 2 * scale * CHAR_WIDTH)
    yPos = (screenHeight / 2) - (scale * CHAR_HEIGHT / 2)
    return Point(int(xPos), int(yPos))

def display_startup():
    global game_state
    clear_display()
    display.set_pen(255, 255, 255)
    text = "PoNg!"
    scale = 4
    center = center_text(text, scale, screen_width, screen_height)
    display.text(text, center.x, center.y, screen_width, scale)
    display.update()
    time.sleep(3.00)
    game_state = GameState.Menu

# Draws the Player Selection Menu on screen
def display_menu():
    global multiplayer
    if display.is_pressed(display.BUTTON_X):
        multiplayer = False
    elif display.is_pressed(display.BUTTON_Y):
        multiplayer = True

    # Display Menu
    display.set_pen(0, 0, 0)
    display.clear()
    display.set_pen(255, 255, 255)
    display.text("Select:", 40, 25, screen_width, 2)
    display.text("1 Player", 57, 40, screen_width, 2)
    display.text("2 Player", 57, 55, screen_width, 2)

    display.text("Press 'A' to START", 40, 85, screen_width, 2)

    if multiplayer:
        display.circle(int(46), int(62), int(3))
    else:
        display.circle(int(46), int(47), int(3))

    display.update()
    time.sleep(0.05)

# Initializes objects to start a new game
def start_game():
    global hitCount
    global balls
    global paddle1
    global paddle2
    global game_state
    hitCount = 0
    balls = []
    balls.append(
        Ball(
            screen_width / 2,
            screen_height / 2,
            ball_size,
            ball_speed,
            ball_speed,
            display.create_pen(255, 255, 255)
        )
    )
    paddle1 = Paddle(
        screen_width - paddle_width,
        (screen_height / 2) - ( paddle_height / 2),
        paddle_height,
        paddle_width,
        display.create_pen(255, 255, 255)
    )

    if multiplayer:
        paddle2 = Paddle(
            0,
            (screen_height / 2) - ( paddle_height / 2),
            paddle_height,
            paddle_width,
            display.create_pen(255, 255, 255)
        )

    game_state = GameState.Playing
    display.set_led(0,0,0)

# Determines if the ball has hit a paddle
def detect_paddle_collision(ball : Ball, paddle : Paddle):
    if paddle.x == 0: # This paddle will only exist in Multiplayer Mode
        return ( ball.x - ball.r ) <= ( paddle.x + paddle.w ) and ( ball.y + ball.r ) >= paddle.y and ( ball.y - ball.r ) <= ( paddle.y + paddle.h ) and ball.dx < 0
    else:
        return ( ball.x + ball.r ) >= paddle.x and ( ball.y + ball.r ) >= paddle.y and ( ball.y - ball.r ) <= ( paddle.y + paddle.h ) and ball.dx > 0

# Displays the Game Over message
def game_over():
    global game_state
    i = 0
    lost_msg = "Game Over!"
    while i < 3:
        clear_display()
        display.set_pen(255, 255, 255)
        display.set_led(255,0,0)
        txt_scale = 3        
        center = center_text(lost_msg, txt_scale, screen_width, screen_height)
        display.text(lost_msg, center.x, center.y, screen_width, txt_scale)
        display.update()
        time.sleep(0.5)
        clear_display()
        display.set_pen(255, 255, 255)
        display.set_led(0,0,0)
        txt_scale = 4
        center = center_text(lost_msg, txt_scale, screen_width, screen_height)
        display.text(lost_msg, center.x, center.y, screen_width, txt_scale)
        display.update()
        time.sleep(0.5)
        i += 1
    game_state = GameState.Menu  # game is lost, return to main menu

# Main game loop
while True:
    if game_state == GameState.Startup:
        display_startup()
        continue

    elif game_state == GameState.Menu:
        if display.is_pressed(display.BUTTON_A):
            start_game()
        else:
            display_menu()
            continue

    elif game_state == GameState.Playing:
        # move paddle
        if display.is_pressed(display.BUTTON_Y):              # if a button press is detected then...
            # paddle is moving down
            if paddle1.y + paddle1.h < screen_height:
                paddle1.y += paddle_move_speed
        elif display.is_pressed(display.BUTTON_X):
            # paddle is moving up
            if paddle1.y > 0:
                paddle1.y -= paddle_move_speed

        if multiplayer:
            # move paddle 2
            if display.is_pressed(display.BUTTON_B):              # if a button press is detected then...
                # paddle is moving down
                if paddle2.y + paddle2.h < screen_height:
                    paddle2.y += paddle_move_speed
            elif display.is_pressed(display.BUTTON_A):
                # paddle is moving up
                if paddle2.y > 0:
                    paddle2.y -= paddle_move_speed

        # Right now just a single ball, but can handle multiple
        for ball in balls:
            ball.x += ball.dx
            ball.y += ball.dy

            xmax = screen_width - ball.r
            xmin = ball.r
            ymax = screen_height - ball.r
            ymin = ball.r

            if ball.y < ymin or ball.y > ymax:
                ball.dy *= -1

            # check if ball hit paddle2 (multiplayer)
            if multiplayer:
                if detect_paddle_collision(ball, paddle2):
                    ball.dx *= -1
                    hitCount += 1
                elif ball.x < xmin:
                    game_over()                   
            else:
                if ball.x < xmin:
                    ball.dx *= -1   # ball is at left side of screen

            # check if ball hit paddle1
            if detect_paddle_collision(ball, paddle1):
                ball.dx *= -1
                hitCount += 1
            elif ball.x > xmax:
                game_over()
            

    # refresh the display
    clear_display()

    for ball in balls:
        display.set_pen(ball.pen)
        display.circle(int(ball.x), int(ball.y), int(ball.r))

    display.set_pen(paddle1.pen)
    display.rectangle(int(paddle1.x), int(paddle1.y), int(paddle1.w), int(paddle1.h))

    if multiplayer:
        display.rectangle(int(paddle2.x), int(paddle2.y), int(paddle2.w), int(paddle2.h))

    display.set_pen(0, 255, 0)
    display.text(str(hitCount), int((screen_width / 2)), 3, 0, 3)

    display.update()
    time.sleep(0.01)