from tkinter import *
from timer import Timer

SIZE = 30
WIDTH = 10
HEIGHT = 20
BORDER = 1

CANVAS_WIDTH = SIZE * WIDTH + 1
CANVAS_HEIGHT = SIZE * HEIGHT + 1

SIDE_PANEL_WIDTH = 200
SIDE_PANEL_HEIGHT = CANVAS_HEIGHT

NEXT_FIGURE_RECT_SIZE = 20

NEXT_FIGURE_CANVAS_WIDTH = NEXT_FIGURE_RECT_SIZE * 4 + 11
NEXT_FIGURE_CANVAS_HEIGHT = NEXT_FIGURE_RECT_SIZE * 4 + 11

CONTAINER_WIDTH = CANVAS_WIDTH + 6 + SIDE_PANEL_WIDTH
CONTAINER_HEIGHT = CANVAS_HEIGHT + 6


class Tetris(Frame):
    def __init__(self, **kwargs):
        Frame.__init__(self, **kwargs)

        self.grid()
        self.grid_columnconfigure(0, minsize=CANVAS_WIDTH)
        self.grid_columnconfigure(1, minsize=SIDE_PANEL_WIDTH)
        self.grid_rowconfigure(0, minsize=CANVAS_HEIGHT)

        self.create_field()
        self.create_side_panel()

        self.start_game()

    def create_field(self):
        canvas = Canvas(
            self,
            bd=0,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg='#ececec'
        )
        canvas.grid(
            row=0,
            column=0
        )

        self.field = []

        for i in range(HEIGHT):
            row = []
            self.field.append(row)

            for j in range(WIDTH):
                y = i * SIZE + 3
                x = j * SIZE + 3

                cell = canvas.create_rectangle(
                    x,
                    y,
                    x + SIZE,
                    y + SIZE
                )

                row.append(cell)

    def create_side_panel(self):
        frame = self.side_panel = Frame(
            self,
            bd=10,
            width=SIDE_PANEL_WIDTH,
            height=SIDE_PANEL_HEIGHT
        )
        frame.grid(
            row=0,
            column=1
        )
        frame.grid_columnconfigure(0, minsize=SIDE_PANEL_WIDTH)

        self.create_points_frame()
        self.create_next_figure_panel()

    def create_points_frame(self):
        points_frame = Frame(
            self.side_panel,
            bd=10,
            highlightbackground='#000',
            highlightthickness=1
        )
        points_frame.grid(
            row=0,
            column=0
        )

        Label(
            points_frame,
            text='Points'
        ).grid(
            row=0,
            column=0
        )

        self.points = StringVar(value=0)
        Label(
            points_frame,
            textvariable=self.points
        ).grid(
            row=1,
            column=0
        )

    def create_next_figure_panel(self):
        next_figure_frame = Frame(
            self.side_panel,
            bd=10,
            highlightbackground='#000',
            highlightthickness=1
        )
        next_figure_frame.grid(
            row=1,
            column=0,
            pady=10
        )

        Label(
            next_figure_frame,
            text='Next:'
        ).grid(
            row=1,
            column=0
        )

        self.next_figure = Canvas(
            next_figure_frame,
            bd=0,
            width=NEXT_FIGURE_CANVAS_WIDTH,
            height=NEXT_FIGURE_CANVAS_HEIGHT,
            bg='#ececec'
        )
        self.next_figure.grid(
            row=4,
            column=0
        )

    def on_quit(self):
        print('quitting')
        root.destroy()
        self.timer.cancel()

    def start_game(self):
        print(1)
        self.timer = Timer(1, self.start_game)


root = Tk()

my_app = Tetris(master=root)
my_app.master.wm_title('Tetris')
my_app.master.minsize(CONTAINER_WIDTH, CONTAINER_HEIGHT)
my_app.master.maxsize(CONTAINER_WIDTH, CONTAINER_HEIGHT)

root.protocol('WM_DELETE_WINDOW', my_app.on_quit)

root.mainloop()
