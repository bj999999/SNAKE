#SNAKE
from tkinter import * #(GUI)
import random
from PIL import Image, ImageTk

# Constantes para el juego
GAME_WIDTH = 400
GAME_HEIGHT = 400
BASE_SPEED_X1 = 150
SPEED_INCREASE = 5  
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
WALL_COLOR = "#FFFF00"  
BACKGROUND_COLOR = "#002366"

class Snake:

    def __init__(self):
        # Inicializar snake con su tamaño de cuerpo, coordenadas y cuadros que representan las partes del cuerpo
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        # Crear una posición aleatoria para food
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.food_image = ImageTk.PhotoImage(Image.open("food.png").resize((SPACE_SIZE, SPACE_SIZE)))
        self.square = canvas.create_image(x, y, image=self.food_image, anchor=NW, tag="food")

    def move_food(self):
        # Mueve food a una nueva posición aleatoria
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        canvas.coords(self.square, x, y)
        self.coordinates = [x, y]

def create_wall():
    # Crear un wall en una posición aleatoria
    x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
    y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
    wall = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=WALL_COLOR, tag="wall")

def next_turn(snake, food):
    global BASE_SPEED_X1
    x, y = snake.coordinates[0]

    # Mover snake según la dirección actual
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    # Comprobar si snake consume food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Puntuación:{}".format(score))
        canvas.delete("food")
        food.move_food()
        food = Food()  # Actualizar la variable 'food' con un nuevo objeto Food
        BASE_SPEED_X1 -= int(BASE_SPEED_X1 * SPEED_INCREASE / 100)  # Calcular nueva velocidad base

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Comprobar colisiones con walls o el cuerpo de snake
    if check_collisions(snake):
        game_over()

    else:
        window.after(BASE_SPEED_X1, next_turn, snake, food)

def change_direction(new_direction):
    # Cambiar la dirección de snake si la nueva dirección es válida
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Comprobar colisiones con los límites del juego
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT: 
        return True

    # Comprobar colisiones con el cuerpo de snake
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    # Comprobar colisiones con walls
    for wall in canvas.find_withtag("wall"):
        if canvas.coords(wall) == [x, y, x + SPACE_SIZE, y + SPACE_SIZE]:
            return True

    return False

def game_over():
    global restart_button
    # Mostrar el texto de "Game Over" y crear el botón de reinicio
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('Geometr415 Blk BT', 30), text="¡GAME OVER!", fill="red", tag="gameover")
    restart_button = Button(frame, text="Iniciar", font=('Geometr415 Blk BT', 12), command=restart_game)
    restart_button.pack(side='left')

def restart_game():
    global snake, food, direction, score, restart_button, BASE_SPEED_X1
    # Reiniciar el juego después de un "Game Over"
    canvas.delete(ALL)
    direction = 'down'
    score = 0
    BASE_SPEED_X1 = 150  # Restaurar la velocidad base a su valor inicial
    label.config(text="Puntuación:{}".format(score))
    restart_button.pack_forget()
    snake = Snake()
    food = Food()
    for _ in range(10):  # Crear 10 walls aleatorios
        create_wall()
    next_turn(snake, food)

# Configurar la ventana principal
window = Tk()
window.title("Snake")
window.resizable(False, False)

frame = Frame(window)
frame.pack(fill=BOTH, expand=True)

# logo
logo = Image.open("logo.png")
logo = logo.resize((200, 50))
logo = ImageTk.PhotoImage(logo)

logo_icon_label = Label(frame, image=logo)
logo_icon_label.pack(side=TOP, padx=100, pady=10)

# Inicializar variables del juego
score = 0
direction = 'down'
snake = None
food = None
restart_button = None

frame = Frame(window)
frame.pack()

label = Label(frame, text="Puntuación:{}".format(score), font=('Geometr415 Blk BT', 12))
label.pack(side='left')

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Centrar la ventana en la pantalla
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")


# Asignar teclas de flecha para cambiar la dirección de snake
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Crear los objetos de snake y food
snake = Snake()
food = Food()

# Crear 10 walls aleatorias al inicio
for _ in range(10):
    create_wall()

# Iniciar el juego
next_turn(snake, food)

window.mainloop()
