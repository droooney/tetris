from random import randint
from copy import deepcopy
from formatter import Formatter
from timer import Timer
from constants import *

INFINITY = float('inf')


class Figure(Formatter):
    def __init__(self, *, name, cells, center, color, app):
        self.name = name
        self.cells = deepcopy(cells)
        self.color = color
        self.app = app
        self.center = center
        self.rotation = gen_rand_rotation()
        self.is_inserted = False
        self.changing = False

        self.calculate_min_and_max()
        self.rotate()
        self.put_in_side_canvas()

    def rotate_right(self):
        self.rotation = 1
        self.rotate()

    def rotate(self):
        new_cells = []
        new_center = self.transform(self.center, True)
        offset_y = 0
        offset_x = 0

        for cell in self.cells:
            new_cells.append(self.transform(cell))

        if self.is_inserted:
            field = self.app.field

            for (y, x) in new_cells:
                if y < 0 and offset_y < -y:
                    offset_y = -y

                if y >= HEIGHT and offset_y > HEIGHT - 1 - y:
                    offset_y = HEIGHT - 1 - y

                if x < 0 and offset_x < -x:
                    offset_x = -x

                if x >= WIDTH and offset_x > WIDTH - 1 - x:
                    offset_x = WIDTH - 1 - x

            for (ix, cell) in enumerate(new_cells):
                (y, x) = new_cells[ix] = self.move_cell(cell, offset_y, offset_x)

                if field[y][x] and not self.find_own_rect(field[y][x]):
                    print('impossible')
                    return

        new_center = self.move_cell(new_center, offset_y, offset_x)

        self.delete_cells()
        self.replace_cells(new_cells, new_center)
        self.calculate_min_and_max()

    def move(self, offset_y, offset_x):
        new_cells = []
        new_center = self.move_cell(self.center, offset_y, offset_x)

        for cell in self.cells:
            new_cell = self.move_cell(cell, offset_y, offset_x)
            new_cells.append(new_cell)

        self.delete_cells()
        self.replace_cells(new_cells, new_center)
        self.calculate_min_and_max()
        # print(self)

    def move_cell(self, cell, offset_y, offset_x):
        return cell[0] + offset_y, cell[1] + offset_x

    def find_own_rect(self, Rect):
        for (y, x, rect) in self.cells:
            if rect == Rect:
                return True

    def delete_cells(self):
        field = self.app.field

        for (y, x, *rest) in self.cells:
            if not len(rest):
                continue

            field[y][x] = None

    def replace_cells(self, new_cells, new_center):
        if self.changing or not self.is_inserted:
            return

        self.changing = True
        field = self.app.field
        field_canvas = self.app.field_canvas

        for (i, cell) in enumerate(self.cells):
            (y, x, *rest) = cell
            (cell[0], cell[1]) = (new_y, new_x) = new_cells[i]

            if not len(rest):
                continue

            rect = rest[0]
            field[new_y][new_x] = rect
            field_canvas.move(rect, (new_x - x) * SIZE, (new_y - y) * SIZE)

        self.center = new_center
        self.changing = False

    def calculate_min_and_max(self):
        self.y_min = min(*self.cells, key=lambda cell: cell[0])[0]
        self.x_min = min(*self.cells, key=lambda cell: cell[1])[1]

        self.y_max = max(*self.cells, key=lambda cell: cell[0])[0]
        self.x_max = max(*self.cells, key=lambda cell: cell[1])[1]

        self.y_len = self.y_max - self.y_min + 1
        self.x_len = self.x_max - self.x_min + 1

    def put_in_side_canvas(self):
        side_canvas = self.app.next_figure_canvas

        side_canvas.delete('all')

        y0 = NEXT_FIGURE_RECT_SIZE * ((4 - self.y_len) / 2 - self.y_min) + 5
        x0 = NEXT_FIGURE_RECT_SIZE * ((4 - self.x_len) / 2 - self.x_min) + 5

        for cell in self.cells:
            y = y0 + cell[0] * NEXT_FIGURE_RECT_SIZE + 3
            x = x0 + cell[1] * NEXT_FIGURE_RECT_SIZE + 3

            side_canvas.create_rectangle(
                x,
                y,
                x + NEXT_FIGURE_RECT_SIZE,
                y + NEXT_FIGURE_RECT_SIZE,
                fill=self.color
            )

        pass

    def transform(self, cell, is_center=False):
        (center_y, center_x, *rest1) = self.center
        rotation = self.rotation
        (y, x, *rest2) = cell
        res = (y, x) = (y - center_y, x - center_x)

        if rotation == 1:
            res = (x, -y)
        elif rotation == 2:
            res = (-y, -x)
        elif rotation == 3:
            res = (-x, y)

        if is_center:
            return center_y + res[0], center_x + res[1]

        return int(center_y + res[0]), int(center_x + res[1])

    def create_timer(self):
        self.app.timer = Timer(self.app.interval, self.move_each_interval)

    def move_to_the_side(self, offset_x):
        field = self.app.field

        for y in range(self.y_min, self.y_max + 1):
            (func, val) = (max, -INFINITY) if offset_x > 0 else (min, INFINITY)
            x = func(*self.cells, key=lambda cell: cell[1] if cell[0] == y else val)[1] + offset_x

            if x >= WIDTH or x < 0 or field[y][x]:
                break
        else:
            self.move(0, offset_x)

    def move_down(self):
        field = self.app.field

        for x in range(self.x_min, self.x_max + 1):
            y = max(*self.cells, key=lambda cell: cell[0] if cell[1] == x else -INFINITY)[0] + 1

            if y >= HEIGHT or field[y][x]:
                return

        self.move(1, 0)

        return True

    def move_each_interval(self):
        if self.move_down():
            self.create_timer()
        else:
            self.stop()

    def stop(self):
        self.is_inserted = False
        self.app.check_lines()

    def insert(self):
        field = self.app.field
        field_canvas = self.app.field_canvas

        cells = self.cells
        new_cells = []
        top_point = TOP_LEFT_INSERT_POINT

        if self.x_len < 3:
            top_point += 1

        for cell in self.cells:
            y = cell[0] - self.y_min
            x = top_point + cell[1] - self.x_min
            canvas_cell = field[y][x]

            if canvas_cell:
                self.app.end_game()
                return

            new_cells.append([y, x])

        for (ix, new_cell) in enumerate(new_cells):
            (i, j) = new_cell
            cell = cells[ix]
            y = i * SIZE + 3
            x = j * SIZE + 3

            field[i][j] = field_canvas.create_rectangle(
                x,
                y,
                x + SIZE,
                y + SIZE,
                fill=self.color
            )

            (cell[0], cell[1]) = (i, j)
            cell.append(field[i][j])

        self.center = (self.center[0] - self.y_min, top_point + self.center[1] - self.x_min)
        self.calculate_min_and_max()
        self.is_inserted = True
        self.create_timer()


FIGURES = {
    # I-figure
    #
    # @@@@
    #
    #
    'I': {
        'cells': [
            [0, -1],
            [0, 0],
            [0, 1],
            [0, 2]
        ],
        'center': (0, 0),
        'color': 'cyan'
    },

    # T-figure
    #
    # @@@
    #  @
    #
    'T': {
        'cells': [
            [0, -1],
            [0, 0],
            [0, 1],
            [1, 0]
        ],
        'center': (0, 0),
        'color': 'purple'
    },

    # L-figure
    #
    # @@@
    # @
    #
    'L': {
        'cells': [
            [0, -1],
            [0, 0],
            [0, 1],
            [1, -1]
        ],
        'center': (0, 0),
        'color': 'orange'
    },

    # J-figure
    #
    # @@@
    #   @
    #
    'J': {
        'cells': [
            [0, -1],
            [0, 0],
            [0, 1],
            [1, 1]
        ],
        'center': (0, 0),
        'color': 'blue'
    },

    # O-figure
    #
    # @@
    # @@
    #
    'O': {
        'cells': [
            [0, -1],
            [0, 0],
            [1, -1],
            [1, 0]
        ],
        'center': (0.5, -0.5),
        'color': 'yellow'
    },

    # S-figure
    #
    #  @@
    # @@
    #
    'S': {
        'cells': [
            [0, 0],
            [0, 1],
            [1, -1],
            [1, 0]
        ],
        'center': (0, 0),
        'color': '#0f0'
    },

    # Z-figure
    #
    # @@
    #  @@
    #
    'Z': {
        'cells': [
            [0, -1],
            [0, 0],
            [1, 0],
            [1, 1]
        ],
        'center': (0, 0),
        'color': 'red'
    }
}

FIGURES_NAMES = list(FIGURES.keys())

for (f, value) in FIGURES.items():
    FIGURES[f] = (lambda f, value: lambda app: Figure(
        name=f,
        cells=value['cells'],
        center = value['center'],
        color=value['color'],
        app=app
    ))(f, value)

ROTATIONS = {
    'TOP': 0,
    'RIGHT': 1,
    'BOTTOM': 2,
    'LEFT': 3
}


def gen_rand_figure_constructor():
    return gen_rand_dict_value(FIGURES)


def gen_rand_rotation():
    return gen_rand_dict_value(ROTATIONS)


def gen_rand_dict_value(_dict):
    keys = list(_dict.keys())
    rand_ix = randint(0, len(keys) - 1)
    key = keys[rand_ix]

    return _dict[key]
