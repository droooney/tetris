from random import randint
from formatter import Formatter

NEXT_FIGURE_RECT_SIZE = 15


class Figure(Formatter):
    def __init__(self, *, name, cells, color, canvas, side_canvas):
        self.name = name
        self.cells = cells
        self.color = color
        self.canvas = canvas
        self.side_canvas = side_canvas
        self.center = self.cells[self.cells.index([0, 1])]
        self.rotation = gen_rand_rotation()
        self.rotate()
        self.put_in_side_canvas()

    def rotate(self):
        pass

    def put_in_side_canvas(self):
        self.side_canvas.delete('all')

        y_min = min(*self.cells, key=lambda cell: cell[0])
        y_max = max(*self.cells, key=lambda cell: cell[0])
        y_len = y_max[0] - y_min[0] + 1

        x_min = min(*self.cells, key=lambda cell: cell[1])
        x_max = max(*self.cells, key=lambda cell: cell[1])
        x_len = x_max[1] - x_min[1] + 1

        y0 = NEXT_FIGURE_RECT_SIZE * ((4 - y_len) / 2) + 5
        x0 = NEXT_FIGURE_RECT_SIZE * ((4 - x_len) / 2) + 5

        for cell in self.cells:
            y = y0 + cell[0] * NEXT_FIGURE_RECT_SIZE + 3
            x = x0 + cell[1] * NEXT_FIGURE_RECT_SIZE + 3

            self.side_canvas.create_rectangle(
                x,
                y,
                x + NEXT_FIGURE_RECT_SIZE,
                y + NEXT_FIGURE_RECT_SIZE,
                fill=self.color
            )

        pass

    def insert(self):
        print(self)
        pass


FIGURES = {
    # I-figure
    #
    # @@@@
    #
    #
    'I': {
        'cells': [
            [0, 0],
            [0, 1],
            [0, 2],
            [0, 3]
        ],
        'color': 'cyan'
    },

    # T-figure
    #
    # @@@
    #  @
    #
    'T': {
        'cells': [
            [0, 0],
            [0, 1],
            [0, 2],
            [1, 1]
        ],
        'color': 'purple'
    },

    # L-figure
    #
    # @@@
    # @
    #
    'L': {
        'cells': [
            [0, 0],
            [0, 1],
            [0, 2],
            [1, 0]
        ],
        'color': 'orange'
    },

    # J-figure
    #
    # @@@
    #   @
    #
    'J': {
        'cells': [
            [0, 0],
            [0, 1],
            [0, 2],
            [1, 2]
        ],
        'color': 'blue'
    },

    # O-figure
    #
    # @@
    # @@
    #
    'O': {
        'cells': [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1]
        ],
        'color': 'yellow'
    },

    # S-figure
    #
    #  @@
    # @@
    #
    'S': {
        'cells': [
            [0, 1],
            [0, 2],
            [1, 0],
            [1, 1]
        ],
        'color': '#0f0'
    },

    # Z-figure
    #
    # @@
    #  @@
    #
    'Z': {
        'cells': [
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 2]
        ],
        'color': 'red'
    }
}

FIGURES_NAMES = list(FIGURES.keys())

for (f, value) in FIGURES.items():
    FIGURES[f] = (lambda f, value: lambda *, canvas, side_canvas: Figure(
        name=f,
        cells=value['cells'],
        color=value['color'],
        canvas=canvas,
        side_canvas=side_canvas
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
