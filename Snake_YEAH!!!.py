import tkinter as tk
import random


class Snake(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x450')  # 增加窗口高度以容纳按钮
        self.title('Snake Game')
        self.game_started = False
        self.snake = [(0, 0), (0, 1), (0, 2)]
        self.direction = 'Right'
        self.food = None
        self.speed = 100  # 初始速度
        self.paused = False  # 暂停标志

        self.canvas = tk.Canvas(self, bg='black', width=400, height=400)
        self.canvas.pack()

        self.start_button = tk.Button(self, text='Start', command=self.start_game)
        self.start_button.pack()

        self.restart_button = tk.Button(self, text='Restart', command=self.restart_game)
        self.restart_button.pack()
        self.restart_button.pack_forget()  # 初次启动时不显示restart_button

        self.bind_all('<Key>', self.on_key_press)

    def start_game(self):
        if not self.game_started:
            self.game_started = True
            self.food = self.create_food()
            self.start_button.pack_forget()
            self.game_loop()

    def create_food(self):
        while True:
            food = (random.randint(0, 19), random.randint(0, 19))
            if food not in self.snake:
                return food

    def update_ui(self):
        self.canvas.delete('all')

        for x, y in self.snake:
            self.canvas.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill='blue')

        fx, fy = self.food
        self.canvas.create_rectangle(fx * 20, fy * 20, fx * 20 + 20, fy * 20 + 20, fill='red')

    def adjust_speed(self):
        length = len(self.snake)
        self.speed = max(30, 100 - (length - 3) * 5)  # 速度随着蛇长增加而增加

    def game_loop(self):
        if not self.game_started or self.paused:
            return

        x, y = self.snake[-1]
        if self.direction == 'Up':
            new_head = (x, y - 1)
        elif self.direction == 'Down':
            new_head = (x, y + 1)
        elif self.direction == 'Left':
            new_head = (x - 1, y)
        else:  # Right
            new_head = (x + 1, y)

        if new_head[0] < 0 or new_head[0] > 19 or new_head[1] < 0 or new_head[1] > 19 or new_head in self.snake:
            self.game_over()
            return

        self.snake.append(new_head)

        if new_head == self.food:
            self.food = self.create_food()
            self.adjust_speed()
        else:
            self.snake.pop(0)

        self.update_ui()
        self.after(self.speed, self.game_loop)

    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=('TkDefaultFont', 24))
        self.restart_button.pack()  # 显示重新开始按钮
        self.game_started = False

    def restart_game(self):
        self.snake = [(0, 0), (0, 1), (0, 2)]
        self.direction = 'Right'
        self.food = self.create_food()
        self.game_started = True
        self.paused = False
        self.speed = 100  # 重设速度
        self.canvas.delete('all')
        self.restart_button.pack_forget()
        self.update_ui()
        self.game_loop()

    def on_key_press(self, event):
        if event.keysym == 'space':
            self.toggle_pause()
        elif self.game_started and not self.paused:
            new_direction = event.keysym
            all_directions = ('Up', 'Down', 'Left', 'Right')
            opposites = ({'Up', 'Down'}, {'Left', 'Right'})
            if new_direction in all_directions and {self.direction, new_direction} not in opposites:
                self.direction = new_direction

    def toggle_pause(self):
        if self.game_started:
            self.paused = not self.paused
            if not self.paused:  # 如果游戏从暂停状态恢复
                self.game_loop()  # 重新启动游戏循环

if __name__ == '__main__':
    Snake().mainloop()