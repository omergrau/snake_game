import copy
import random

import pygame


class body(pygame.sprite.Sprite):
    def __init__(self, x, y, image, next=None):
        super().__init__()
        self.size = 20
        self.direction = "right"
        self.x = x
        self.y = y
        self.next = next
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def __str__(self):
        return f"x is {self.x} y is {self.y}"


class snake:
    def __init__(self, body1):
        self.organs = body1
        self.head = body1
        self.tail = body1
        self.movement_speed = 2

    def __str__(self):
        temp = ""
        for i in range(len(self.organs)):
            temp += f"cell number {i} {self.organs[i]}\n"
        return temp

    def eating(self, x, y):
        body1 = body(x, y, pygame.image.load("images/head_right.png").convert_alpha())
        self.tail.next = body1
        self.tail.image =  pygame.transform.scale(pygame.image.load("images/head_right.png").convert_alpha(), (20, 20))
        self.tail = self.tail.next
        """temp = self.organs
        while temp.next:
            temp = temp.next
        temp.next = body1"""

    def do_move(self, direction):
        temp = self.organs
        if direction == "left":
            x, y = self.organs.x - self.movement_speed, self.organs.y
            self.head.rect.topleft = (x, y)
            self.head.image = pygame.image.load("images/head_left.png").convert_alpha()
            self.head.image = pygame.transform.scale(self.head.image, (self.head.size, self.head.size))
        if direction == "right":
            x, y = self.organs.x + self.movement_speed, self.organs.y
            self.head.rect.topleft = (x, y)
            self.head.image = pygame.image.load("images/head_right.png").convert_alpha()
            self.head.image = pygame.transform.scale(self.head.image, (self.head.size, self.head.size))
        if direction == "up":
            x, y = self.organs.x, self.organs.y - self.movement_speed
            self.head.rect.topleft = (x, y)
            self.head.image = pygame.image.load("images/head_strait.png").convert_alpha()
            self.head.image = pygame.transform.scale(self.head.image, (self.head.size, self.head.size))
        if direction == "down":
            x, y = self.organs.x, self.organs.y + self.movement_speed
            self.head.rect.topleft = (x, y)
            self.head.image = pygame.image.load("images/head_down.png").convert_alpha()
            self.head.image = pygame.transform.scale(self.head.image, (self.head.size, self.head.size))

        while temp is not None:
            temp_x = temp.x
            temp_y = temp.y
            if temp.y > y:
                temp.direction = "down"
                temp.image = pygame.image.load("images/body_up_down.png").convert_alpha()
                temp.image= pygame.transform.scale(temp.image,(20,20))
                #self.rect.topleft = self.image.get_rect().topleft
            if temp.y < y:
                temp.direction = "up"
                temp.image = pygame.image.load("images/body_up_down.png").convert_alpha()
                temp.image= pygame.transform.scale(temp.image,(20,20))
                #self.rect.topleft = self.image.get_rect().topleft
            temp.y = y
            temp.x = x
            y = temp_y
            x = temp_x
            temp.rect.topleft = (x, y)
            temp = temp.next


class food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = 20
        self.image = pygame.image.load("images/apple.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


def move(snake, direction):
    if direction == "left" or direction == "right":
        if snake.organs.y % 20 == 1:
            return True
    if direction == "up" or direction == "down":
        if snake.organs.x % 20 == 1:
            return True


def do_move(snake, direction):
    if direction == "left":
        x, y = (snake.head.x - snake.movement_speed, snake.head.y)
    if direction == "right":
        x, y = (snake.head.x + snake.movement_speed, snake.size[0].y)
    if direction == "up":
        x, y = (snake.head.x, snake.head.y - snake.movement_speed)
    if direction == "down":
        x, y = (snake.head.x, snake.head.y + snake.movement_speed)

    snake.head.do_move(x, y)


def try_move_without_fail(snake):
    curr = snake.organs
    temp = snake.organs.next
    while temp:
        if abs(temp.x - curr.x) < 2 and abs(temp.y - curr.y) < 2:
            return False
        temp = temp.next
    return True


clock = pygame.time.Clock()
pygame.display.set_caption("snake game")


def play_game():
    import pygame
    from snake import snake
    pygame.init()
    hight = 400
    width = 400
    bg_color = (0, 0, 0)
    screen = pygame.display.set_mode((width, hight))
    food_x = random.choice(range(1, width - 19, 20))
    food_y = random.choice(range(1, hight - 19, 20))
    apple = food(food_x, food_y)
    screen.blit(apple.image, apple.rect)
    image1 = pygame.image.load("images/head_right.png").convert_alpha()
    image1 = pygame.transform.scale(image1, (20, 20))
    body1 = body(101, 701, image1)
    snake = snake(body1)
    last_move = "right"
    is_food = True
    counter_food = -1
    temp_location = (0, 0)
    game_points = 0
    player_is_dead = False
    while not player_is_dead:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        key = pygame.key.get_pressed()

        if key[pygame.K_UP]:
            if move(snake, "up") and last_move not in ["down", "up"]:
                snake.do_move("up")
                last_move = "up"

        if key[pygame.K_DOWN]:
            if move(snake, "down") and last_move not in ["down", "up"]:
                snake.do_move("down")
                last_move = "down"

        if key[pygame.K_LEFT]:
            if move(snake, "left") and last_move not in ["left", "right"]:
                snake.do_move("left")
                last_move = "left"
        if key[pygame.K_RIGHT]:
            if move(snake, "right") and last_move not in ["left", "right"]:
                snake.do_move("right")
                last_move = "right"

        if abs(snake.organs.x - food_x) < 20 and abs(snake.organs.y - food_y) < 20:
            counter_food = 1
            game_points += 1
            is_food = False
            food_x, food_y = -100, -100
            temp_location = (snake.organs.x, snake.organs.y)
        if counter_food == 0:
            snake.eating(temp_location[0], temp_location[1])

        cell = copy.copy(snake.organs)
        while cell is not None:
            screen.blit(cell.image, cell.rect)
            # pygame.draw.rect(screen, "green", (cell.x, cell.y, cell.width, cell.hight))
            cell = cell.next

        if not is_food:
            ok = False
            while not ok:
                food_x = random.choice(range(1, width - 19, 20))
                food_y = random.choice(range(1, hight - 19, 20))
                cell = snake.organs
                while cell:
                    if abs(food_x - cell.x) < 20 and abs(food_y - cell.y) < 20:
                        break
                    else:
                        cell = cell.next
                        ok = True
        apple = food(food_x, food_y)
        screen.blit(apple.image, apple.rect)
        is_food = True
        if snake.organs.x > width:
            snake.organs.x = 1
        if snake.organs.x < 0:
            snake.organs.x = width + 1
        if snake.organs.y > width:
            snake.organs.y = 1
        if snake.organs.y < 0:
            snake.organs.y = hight + 1
        if not try_move_without_fail(snake):
            game_over(game_points)

        counter_food -= 1
        text = pygame.font.Font(None, 36)
        text = text.render(f"score: {game_points}", True, (255, 255, 255))
        screen.blit(text, ((hight - text.get_size()[0]) / 2, 0))
        snake.do_move(last_move)
        pygame.time.Clock()
        pygame.display.update()
        clock.tick(150)


def game_over(score):
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("press r to restart", True, (255, 255, 255))
    score_text = font.render(f"your score was {score}", False, "green")
    screen.blit(text, ((400 - text.get_size()[0]) / 2, (400 - text.get_size()[1]) / 2))
    screen.blit(score_text, ((400 - text.get_size()[0]) / 2, (200 - text.get_size()[1]) / 2))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            play_game()
        pygame.display.update()
        # pygame.draw.rect(screen, text)
        clock.tick(60)


play_game()
