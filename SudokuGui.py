import pygame

WIDTH = 900
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
TURQUOISE = (71, 178, 255)
HIGHLIGHT = (208, 241, 255)
run = True
pygame.init()
temp = [[0, 1, 5, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 3, 0, 0, 8, 9, 0],
        [0, 7, 0, 0, 0, 9, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 5, 0],
        [0, 0, 0, 9, 0, 6, 0, 0, 0],
        [0, 0, 0, 4, 1, 0, 0, 0, 9],
        [3, 5, 2, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 4, 2, 0]]

pygame.display.set_caption('Sudoku')


class Node:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.width = 100
        self.x = self.column * self.width
        self.y = self.row * self.width
        self.number = '0'
        self.rect = pygame.Rect(self.x, self.y, 100, 100)
        self.font = pygame.font.SysFont('Arial', 100)
        self.color = (32, 32, 32)
        self.base = False
        self.active = False
        self.highlighted = False

    def get_position(self):
        return self.column, self.row

    def is_active(self):
        self.active = True
        self.color = BLUE

    def is_not_active(self):
        self.active = False
        self.color = (33, 33, 33)

    def is_wrong(self):
        self.color = RED

    def is_right(self):
        self.color = GREEN

    def draw_rect(self):
        if self.active:
            pygame.draw.rect(WINDOW, BLUE, self.rect, 1)
        else:
            pygame.draw.rect(WINDOW, (32, 32, 32), self.rect, 1)

    def draw_number(self):
        if self.number != '0':
            text_surface = self.font.render(self.number, True, self.color)
            WINDOW.blit(text_surface, (self.x + 22, self.y - 5))

    def highlight_node(self):
        if self.highlighted:
            pygame.draw.rect(WINDOW, HIGHLIGHT, self.rect)
            self.draw_rect()
            self.draw_number()


def possible(x, y, n):
    global temp
    grid = temp
    if n in grid[y]:
        return False
    for index, rows in enumerate(grid):
        if grid[index][x] == n:
            return False
    cube_x = (x // 3) * 3
    cube_y = (y // 3) * 3
    for y in range(3):
        for x in range(3):
            if grid[cube_y + y][cube_x + x] == n:
                return False
    return True


def solve():
    global temp
    global GRID
    for y, row in enumerate(temp):
        for x, element in enumerate(row):
            if element == 0:
                for n in range(1, 10):
                    if possible(x, y, n):
                        temp[y][x] = n
                        solve()
                        temp[y][x] = 0

                return
    for row1, row2 in zip(GRID, temp):
        for node1, node2 in zip(row1, row2):
            if node1.number == str(node2) and not node1.base:
                node1.is_right()
            else:
                if node1.number == '0':
                    node1.number = str(node2)
                    node1.color = TURQUOISE
                else:
                    if not node1.base:
                        node1.is_wrong()
    draw_grid(WINDOW, GRID)


def make_grid():
    """This function makes all instances of the nodes in the grid"""
    width = 900
    rows = 9
    grid = []
    for row1 in range(rows):
        grid.append([])
        for column1 in range(rows):
            node1 = Node(row1, column1)
            grid[row1].append(node1)

    return grid


def clear_grid():
    global GRID
    for row1 in GRID:
        for node1 in row1:
            if node1.base is False:
                node1.number = '0'


def update_grid_numbers(grid, template):
    for row1, row2 in zip(grid, template):
        for node1, node2 in zip(row1, row2):
            node1.number = str(node2)
            if node2 != 0:
                node1.base = True
    return grid


def mouse_position(position):
    """This function gets the current mouse position by dividing the current X and Y coordinates
       by the size of the grid cubes to get the current row and column thus the exact cube"""
    cube = 100
    y, x = position
    row = y // cube
    column = x // cube
    return column, row


def draw_grid(win, grid):
    width = WIDTH
    rows = 9
    gap = 900 // 9
    for i in range(9):
        if i % 3 == 0:
            pygame.draw.line(win, (33, 33, 33), (0, i * gap), (width, i * gap), 4)
        for j in range(rows):
            if j % 3 == 0:
                pygame.draw.line(win, (33, 33, 33), (j * gap, 0), (j * gap, width), 4)
    for rows in grid:
        for nodes in rows:
            nodes.draw_rect()
            nodes.draw_number()


GRID = update_grid_numbers(make_grid(), temp)

while run:
    WINDOW.fill(WHITE)
    draw_grid(WINDOW, GRID)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in GRID:
                for node in row:
                    if node.rect.collidepoint(event.pos) and node.base is False:
                        node.is_active()
                        active_node = node
                    else:
                        node.is_not_active()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                clear_grid()
            if event.key == pygame.K_SPACE:
                solve()
            else:
                try:
                    active_node.number += event.unicode
                    if len(active_node.number) > 1:
                        active_node.number = active_node.number[-1]
                    if active_node.number not in [str(i) for i in range(10)]:
                        active_node.number = str(0)
                except:
                    pass
    position = pygame.mouse.get_pos()
    row, column = mouse_position(position)
    node = GRID[row][column]
    if node.rect.collidepoint(position):
        if node.base is False:
            node.highlighted = True
            node.highlight_node()
    else:
        node.highlighted = False
    draw_grid(WINDOW, GRID)
    pygame.display.update()

pygame.quit()
