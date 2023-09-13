import random
import os

RESOLUTION = 600
COLUMNS = 20
ROWS = 20
WIDTH = RESOLUTION/COLUMNS
HEIGHT = RESOLUTION/ROWS
path = os.getcwd()

class Element_board:
    def __init__(self, r, c):
        self.c = c
        self.r = r
        self.s = 0
        self.f = False
    def display(self):
        stroke(205)
        strokeWeight(0)
        fill(205)
        rect(self.c * WIDTH, self.r * HEIGHT, WIDTH, HEIGHT)

class Element_snake:
    def __init__(self, r, c, s = 0, f = False, fruit = ''):
        self.c = c
        self.r = r
        self.s = s
        self.f = f
        self.fruit = fruit
        self.head = RIGHT
        self.head_up = loadImage(path + "/images/" + "head_up.png")
        self.head_left = loadImage(path + "/images/" + "head_left.png")
    def display(self):
        if self.f == False:
            if self.s == 1:
                if self.head == LEFT:
                    image(self.head_left, self.c * WIDTH, self.r * HEIGHT, WIDTH, HEIGHT)
                elif self.head == RIGHT:
                    image(self.head_left, self.c * WIDTH, self.r * HEIGHT, WIDTH, HEIGHT, 30, 30, 0, 0)
                elif self.head == UP:
                    image(self.head_up, self.c * WIDTH, self.r * HEIGHT, WIDTH, HEIGHT)
                elif self.head == DOWN:
                    image(self.head_up, self.c * WIDTH, self.r * HEIGHT, WIDTH, HEIGHT, 30, 30, 0, 0)
            elif self.s > 1:
                fill(80, 153, 32)
                strokeWeight(0)
                ellipse(self.c * WIDTH + WIDTH/2, self.r * HEIGHT + HEIGHT/2, WIDTH, HEIGHT)
        elif self.f == True:
            if self.fruit == 'apple':
                fill(173, 48, 32)
                strokeWeight(0)
                ellipse(self.c * WIDTH + WIDTH/2, self.r * HEIGHT + HEIGHT/2, WIDTH, HEIGHT)
            elif self.fruit == 'banana':
                fill(251, 226, 76)
                strokeWeight(0)
                ellipse(self.c * WIDTH + WIDTH/2, self.r * HEIGHT + HEIGHT/2, WIDTH, HEIGHT)

class Fruit:
    def __init__(self, r, c, s = 0):
        self.c = c
        self.r = r
        self.s = s
        self.f = True
        self.fruit_items = ["apple", "banana"]
        self.fruit = random.choice(self.fruit_items)
        self.img = loadImage(path + "/images/" + self.fruit + ".png")
    def display(self):
        image(self.img, self.c * WIDTH, self.r * HEIGHT)

        
                
class Snake(list):
    def __init__(self):
        self.game_over = False
        self.append(Element_snake(9, 11, 1))
        self.append(Element_snake(9, 10, 2))
        self.append(Element_snake(9, 9, 3,))
        self.key_handler = {LEFT:False, RIGHT:True, UP:False, DOWN:False}
    def head_move(self, head):
        head = head
        if self.key_handler[LEFT]:
            head.c = head.c - 1
            if head.c > -1:
                self.eat(head.r, head.c)
            for tail in self:
                if tail.r == head.r and tail.c == head.c and tail.s != 1:
                    board.snake.game_over = True
            self[0] = head
            head.head = LEFT
        elif self.key_handler[RIGHT]:
            head.c = head.c + 1
            self[0] = head
            if head.c < 20:
                self.eat(head.r, head.c)
            for tail in self:
                if tail.r == head.r and tail.c == head.c and tail.s != 1:
                    board.snake.game_over = True
            head.head = RIGHT
        elif self.key_handler[UP]:
            head.r = head.r - 1
            self[0] = head
            if head.r > -1:
                self.eat(head.r, head.c)
            for tail in self:
                if tail.r == head.r and tail.c == head.c and tail.s != 1:
                    board.snake.game_over = True
            head.head = UP
        elif self.key_handler[DOWN]:
            head.r = head.r + 1
            self[0] = head
            if head.r < 20:
                self.eat(head.r, head.c)
            for tail in self:
                if tail.r == head.r and tail.c == head.c and tail.s != 1:
                    board.snake.game_over = True
            head.head = DOWN
    def move(self):
        for head in self:
            if head.s == 1 and head.c < COLUMNS and head.r < ROWS and head.c > -1 and head.r > -1:
                current_tail = 2
                empty_row = head.r
                empty_col = head.c
                self.head_move(head)
                tail_numbers = 0
                for element in self:
                    if element.s > tail_numbers:
                        tail_numbers = element.s
                while current_tail != tail_numbers+1:
                    for tail in self:
                        if tail.s == current_tail:
                            if tail.f == False:
                                self[tail.s-1] = Element_snake(empty_row, empty_col, tail.s)
                            elif tail.f:
                                self[tail.s-1] = Element_snake(empty_row, empty_col, tail.s, True, tail.fruit)
                                board.fruit()
                            empty_row = tail.r
                            empty_col = tail.c
                            current_tail = current_tail + 1
                            board[tail.r][tail.c] = Element_board(tail.r, tail.c)
                break
            elif head.s == 1:
                self.game_over = True
    def eat(self, row, col):
        fruit_r = row
        fruit_c = col
        if board[fruit_r][fruit_c].f:
            last_tail = self[-1]
            self.append(Element_snake(last_tail.r, last_tail.c, last_tail.s + 1, True, board[fruit_r][fruit_c].fruit))
            board[fruit_r][fruit_c] = Element_board(fruit_r, fruit_c)
        
class Board(list):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.score = 0
        self.snake = Snake()
        for row in range(ROWS):
            collection = []
            for column in range(COLUMNS):
                collection.append(Element_board(row, column))
            self.append(collection)
    def snake_into_board(self):
        for element in self.snake:
            if -1 < element.r < 20 and -1 < element.c < 20:
                self[element.r][element.c] = element
    def fruit(self):
        fruit_on_board = 0
        for collection in self:
            for element in collection:
                if element.f != 0:
                    fruit_on_board = 1
        if fruit_on_board == 0:
            r = random.randint(0, 19)
            c = random.randint(0, 19)
            while self[r][c].f != 0:
                r = random.randint(0, 19)
                c = random.randint(0, 19)
            self[r][c] = Fruit(r, c)
    def display(self):
        if self.snake.game_over == False:
            self.fruit()
            self.snake.move()
            self.snake_into_board()
            for collection in self:
                for element in collection:
                    element.display()
        else:
            fill(0, 0, 0)
            textSize(40)
            text('GAME OVER!', 180, 300)
            textSize(25)
            text('Score: '+ str(board.snake[-1].s - 3), 250, 350)
        
board = Board(RESOLUTION, RESOLUTION)

def setup():
    size(board.w, board.h)
    background(0,0,0)

def draw():
    if frameCount%12 == 0:
        background(205)
        board.display()
        fill(0, 0, 0)
        textSize(15)
        text('Score: '+ str(board.snake[-1].s - 3), 520, 15)

def mouseClicked():
    background(205)
    for row in range(ROWS):
        for column in range(COLUMNS):
            board[row][column] = Element_board(row, column)
    board.score = 0
    board.snake.game_over = False
    board.snake
    board.snake = Snake()
    

def keyPressed():
    if keyCode == LEFT:
        if board.snake.key_handler[RIGHT] == True:
            board.snake.key_handler[LEFT] = False
        else:
            board.snake.key_handler[LEFT] = True
            board.snake.key_handler[RIGHT] = False
            board.snake.key_handler[UP] = False
            board.snake.key_handler[DOWN] = False
    elif keyCode == RIGHT:
        if board.snake.key_handler[LEFT] == True:
            board.snake.key_handler[RIGHT] = False
        else:
            board.snake.key_handler[LEFT] = False
            board.snake.key_handler[RIGHT] = True
            board.snake.key_handler[UP] = False
            board.snake.key_handler[DOWN] = False
    elif keyCode == UP:
        if board.snake.key_handler[DOWN] == True:
            board.snake.key_handler[UP] = False
        else:
            board.snake.key_handler[LEFT] = False
            board.snake.key_handler[RIGHT] = False
            board.snake.key_handler[UP] = True
            board.snake.key_handler[DOWN] = False
    elif keyCode == DOWN:
        if board.snake.key_handler[UP] == True:
            board.snake.key_handler[DOWN] = False
        else:
            board.snake.key_handler[LEFT] = False
            board.snake.key_handler[RIGHT] = False
            board.snake.key_handler[UP] = False
            board.snake.key_handler[DOWN] = True
