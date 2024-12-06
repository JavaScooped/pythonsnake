import tkinter as tk
import random

snake_x = 225
snake_y = 225
snake_size = 10
dx, dy = 0, 0
snake_segments = [(225, 225)]
apple_x = 0
apple_y = 0
score = 0

def create_window():
    global apple_x, apple_y, score
    root = tk.Tk()
    root.title("Snake")
    root.geometry("450x450")
    root.configure(background='black')
    
    canvas = tk.Canvas(root, width=450, height=450, bg="black")
    canvas.pack()
    canvas.create_text(225, 225, text="Press any arrow key to begin!", fill="green", font=('Helvetica', 10))
    root.bind("<Up>", lambda event: set_direction(0, -10))
    root.bind("<Down>", lambda event: set_direction(0, 10))
    root.bind("<Left>", lambda event: set_direction(-10, 0))
    root.bind("<Right>", lambda event: set_direction(10, 0))
    
    apple_x, apple_y = spawn_apple()
    update_game(canvas, root)
    root.mainloop()

def draw_snake(canvas):
    global snake_segments, snake_size
    for segment in snake_segments:
        x, y = segment
        canvas.create_rectangle(
            x - snake_size // 2, y - snake_size // 2,
            x + snake_size // 2, y + snake_size // 2,
            fill="green"
        )

def draw_apple(canvas, x, y):
    canvas.create_rectangle(
        x - snake_size // 2, y - snake_size // 2,
        x + snake_size // 2, y + snake_size // 2,
        fill="red"
    )

def draw_score(canvas):
    global score
    canvas.create_text(225, 10, text=f"Score: {score}", fill="white", font=('Helvetica', 12))

def set_direction(new_dx, new_dy):
    global dx, dy
    if (dx == 0 and new_dx != 0) or (dy == 0 and new_dy != 0):
        dx, dy = new_dx, new_dy

def update_game(canvas, root):
    global snake_x, snake_y, apple_x, apple_y, snake_segments, dx, dy, score
    if dx == 0 and dy == 0:
        canvas.after(100, update_game, canvas, root)
        return

    new_head = (snake_segments[0][0] + dx, snake_segments[0][1] + dy)

    if new_head[0] < 0 or new_head[0] >= 450 or new_head[1] < 0 or new_head[1] >= 450:
        game_over(canvas, root)
        return
    
    if new_head in snake_segments:
        game_over(canvas, root)
        return

    snake_segments = [new_head] + snake_segments[:-1]

    if new_head[0] == apple_x and new_head[1] == apple_y:
        growsnake()
        apple_x, apple_y = spawn_apple()
        score += 1

    canvas.delete("all")
    draw_snake(canvas)
    draw_apple(canvas, apple_x, apple_y)
    draw_score(canvas)
    canvas.after(100, update_game, canvas, root)

def spawn_apple():
    global snake_segments
    grid_size = 10
    max_position = 450 // grid_size
    while True:
        x = random.randint(0, max_position - 1) * grid_size + grid_size // 2
        y = random.randint(0, max_position - 1) * grid_size + grid_size // 2
        if (x, y) not in snake_segments:
            return x, y

def growsnake():
    global snake_segments
    snake_segments.append(snake_segments[-1])

def game_over(canvas, root):
    canvas.delete("all")
    canvas.create_text(225, 225, text="Game Over!", fill="red", font=('Helvetica', 20))
    canvas.create_text(225, 250, text=f"Score: {score}", fill="white", font=('Helvetica', 12))
    root.after(2000, root.quit)

create_window()