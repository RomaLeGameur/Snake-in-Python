from tkinter import *
import random
import threading

GAME_WIDTH = 1500
GAME_HEIGTH = 900
SPEED = 75
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF5F"
FOOD_COLOR = "#ff0000"
SUPER_FOOD_COLOR = "#ffff00"
BACKGROUND_COLOR = "#3F1E1E"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill= SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    
    def __init__(self):
        
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)-1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGTH / SPACE_SIZE)-1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

class Super_Food:
    
    def __init__(self):
        
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)-1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGTH / SPACE_SIZE)-1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SUPER_FOOD_COLOR, tag="super_food")

def is_super_food_eaten(snake, super_food):
    # Retourne True si la tête du serpent est sur la super_food, sinon False.
    if super_food is None:
        return False
    x, y = snake.coordinates[0]
    return x == super_food.coordinates[0] and y == super_food.coordinates[1]

def double_speed_for_5_seconds():
    global SPEED
    original_speed = SPEED
    SPEED = max(10, SPEED // 2)  # Double la vitesse (divise le délai par 2, minimum 10ms)
    def restore_speed():
        global SPEED
        SPEED = original_speed
    # Après 5 secondes, restaurer la vitesse d'origine
    threading.Timer(5.0, restore_speed).start()

# Fonction pour gérer le prochain tour du serpent
# Elle déplace le serpent, gère la nourriture et les collisions.
def next_turn(snake, food, super_food):
    global SPEED  # Ajout pour pouvoir modifier la vitesse

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill= SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Si le serpent mange la super_food
    if is_super_food_eaten(snake, super_food):
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("super_food")
        super_food = None
        double_speed_for_5_seconds()
        food = Food()
        
    # Si le serpent mange la food normale
    elif x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        # Apparition du super_food tous les 5 points
        if score % 5 == 0:
            super_food = Super_Food()
        else:
            food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food, super_food)

def change_direction(new_direction):
    
    global direction
    
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    
    x, y = snake.coordinates[0]
    
    if x < 0:
        x = GAME_WIDTH

    elif x >= GAME_WIDTH:
        x = 0 - SPACE_SIZE
    
    if y < 0:
        y = GAME_HEIGTH

    elif y >= GAME_HEIGTH:
        y = 0 - SPACE_SIZE
    
    snake.coordinates[0] = (x, y)



    
    for boby_part in snake.coordinates[1:]:
        if x == boby_part[0] and y == boby_part[1]:
            return True
        
    return False

def game_over():
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, 
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGTH, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Up>', lambda event: change_direction('up'))

snake = Snake()
food = Food()


next_turn(snake, food, super_food=None)

window.mainloop()